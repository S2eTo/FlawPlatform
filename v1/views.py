import os
import uuid
import base64
from datetime import datetime

from captcha.views import (
    CaptchaStore, captcha_image
)
from django.conf import settings
from django.contrib.auth import login, logout
from django.core.files.images import get_image_dimensions
from django.contrib.auth.forms import AuthenticationForm, AdminPasswordChangeForm

from common import mail
from dockerapi.models import (
    Image, Container, Checked
)
from users.models import User, EmailToken
from common.file import get_extension
from common.decorators import validate
from users.forms import UserCreationForm
from v1.paginations import CommonPageNumberPagination
from common.views import (
    UserAPIView, AnonymousAPIView, CheckGetPermissionsAPIView, CheckPostPermissionsAPIView
)
from v1.serializers import (
    ImagesSerializer, ContainerSerializer, CheckedSerializer, UserSerializer, UsersSerializer
)
from v1.validators import (
    IdValidation, GetImagesValidation, FlagValidation, RegisterEmailValidation, EmailTokenValidation, CaptchaValidation,
    ResetPasswordEmailValidation
)


class GetCaptcha(AnonymousAPIView):
    """
    获取验证码
    """

    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        try:
            # 获取图片id
            id_ = CaptchaStore.objects.filter(hashkey=hashkey).first().id
            image = captcha_image(request, hashkey)
            # 将图片转换为base64
            image_base = 'data:image/png;base64,%s' % base64.b64encode(image.content).decode('utf-8')
            json_data = {
                "id": id_,
                "image_base": image_base
            }

            # 批量删除过期验证码
            CaptchaStore.remove_expired()
        except Exception:
            json_data = None

        return self.success('获取成功', data=json_data)


class Register(AnonymousAPIView):
    """
    注册接口, 不需要身份认证
    """

    @validate(validator=(CaptchaValidation, RegisterEmailValidation))
    def post(self, request, data: RegisterEmailValidation):
        email = data.cleaned_data.get('email')

        # step1: 刷新/创建激活码
        try:
            # 邮箱已经存在过了就刷新验证码
            email_token = EmailToken.objects.get(email=email)

            # 一分钟内不运行刷新 Token, 防止恶意操作
            if email_token.interval():
                return self.failed('邮件已发送,若收件箱中未找到，请检查垃圾邮件。请一分钟后重试', data={
                    'timer': email_token.update_time
                }, code=-1)

            email_token.mode = 1
            email_token.save()
        except EmailToken.DoesNotExist:
            email_token = EmailToken()
            email_token.email = email
            email_token.mode = 1
            email_token.save()

        # 删除过期 Token
        EmailToken.remove_expired()

        # step2: 发送注册邮件
        bind_uri = '{}/#/bind?email_token={}'.format(settings.REGISTER_BASE_URI, email_token.key)

        mail.send('[FlawPlatform 漏洞靶场] 注册邮件', '您好 {}'.format(email),
                  '欢迎您注册，FlawPlatform 漏洞靶场，点击连接 <a href="{}">{}</a> 完成注册，此链接30分钟内有效。请忽将连接告知其人，如不是您本人操作无视当前邮件即可。'.format(
                      bind_uri, bind_uri), [email])

        return self.success("已发送激活链接至邮箱 {}. 若收件箱中未找到，请检查垃圾邮件。".format(email), data={
            'timer': email_token.update_time
        })


class BindEmail(AnonymousAPIView):

    @validate(validator=(CaptchaValidation, EmailTokenValidation, UserCreationForm))
    def post(self, request, data: [EmailTokenValidation, UserCreationForm]):
        # step1: 获取注册码对象
        email_token: EmailToken = data[0].cleaned_data.get('key')

        # step2: 判断验证码类型
        if email_token.mode != 1:
            return self.failed('注册链接已过期，请重新获取')

        # step3: 保存用户
        user: UserCreationForm = data[1]
        user: User = user.save(False)
        user.email = email_token.email
        user.save()

        return self.success('注册成功')


class Login(AnonymousAPIView):
    """
    用户登录
    """

    @validate(validator=(CaptchaValidation, AuthenticationForm))
    def post(self, request, data: AuthenticationForm):
        login(request, user=data.get_user())

        return self.login_userinfo(request)


class Logout(UserAPIView, CheckPostPermissionsAPIView):
    """
    退出登录
    """

    def post(self, request):
        logout(request)
        return self.success('退出登录成功。')


class CheckIn(UserAPIView, CheckPostPermissionsAPIView):
    """
    检查是否已登录
    """

    def post(self, request):
        return self.login_userinfo(request)


class GetUserInfo(UserAPIView, CheckGetPermissionsAPIView):
    """
    获取用户信息
    """

    def get(self, request):
        checked = Checked.objects.filter(user=request.user)

        return self.success('获取成功', data={'user': UserSerializer(request.user).data})


class Avatar(UserAPIView, CheckPostPermissionsAPIView):
    """
    用户修改头像
    """

    def post(self, request):
        avatar = request.FILES.get('avatar')

        # 数据验证
        if avatar:
            # 判断允许的格式
            if get_extension(avatar.name) not in settings.VALID_IMAGE_FORMATS:
                return self.failed('只允许 jpg 格式的头像！')

            try:
                # 判断图片大小
                w, h = get_image_dimensions(avatar)
                if w > settings.VALID_IMAGE_WIDTH or h > settings.VALID_IMAGE_HEIGHT:
                    return self.failed('图片太大了, 必须小于等于{}px × {}px'.format(str(settings.VALID_IMAGE_WIDTH),
                                                                         str(settings.VALID_IMAGE_HEIGHT)))
            except Exception:
                return self.failed('你这那是图片啊！')

        if not request.user.is_default_avatar():
            # 如果当前不是默认头像, 就删除掉当前头像
            opath = os.path.join(settings.MEDIA_ROOT, str(request.user.avatar))
            if os.path.isfile(opath):
                os.remove(opath)

        # 随机文件名
        avatar.name = "{}-{}.{}".format(datetime.now().strftime('%Y%m%d%H%M%S%f'), uuid.uuid4(),
                                        get_extension(avatar.name))

        request.user.avatar = avatar
        request.user.save()

        return self.success('更换成功', data={'user': UserSerializer(request.user).data})


class GetResetPasswordEmail(AnonymousAPIView):

    @validate(validator=(CaptchaValidation, ResetPasswordEmailValidation))
    def post(self, request, data: ResetPasswordEmailValidation):
        email = data.cleaned_data.get('email')

        # step1: 刷新/创建激活码
        try:
            # 邮箱已经存在过了就刷新验证码
            email_token = EmailToken.objects.get(email=email)

            # 一分钟内不运行刷新 Token, 防止恶意操作
            if email_token.interval():
                return self.failed('邮件已发送, 若收件箱中未找到，请检查垃圾邮件。请一分钟后重试', data={
                    'timer': email_token.update_time
                }, code=-1)

            email_token.mode = 2
            email_token.save()
        except EmailToken.DoesNotExist:
            email_token = EmailToken()
            email_token.email = email
            email_token.mode = 2
            email_token.save()

        # 删除过期 Token
        EmailToken.remove_expired()

        # step2: 发送注册邮件
        bind_uri = '{}/#/reset?email_token={}'.format(settings.REGISTER_BASE_URI, email_token.key)

        mail.send('[FlawPlatform 漏洞靶场] 重置密码信息', '尊敬的用户 {}'.format(email),
                  '有人尝试重置您本邮箱注册的账号密码，请确认是本人操作，确认后在30分钟内点击如下链接重置密码。<br/> <a href="{}">{}</a> <br/>如果不是您本人发起的操作，请忽略此邮件。<br/>您的密码在不点击链接并操作的情况下不会进行修改。'.format(
                      bind_uri, bind_uri), [email]
                  )

        return self.success("已发送激活链接至邮箱 {}. 若收件箱中未找到，请检查垃圾邮件。".format(email), data={
            'timer': email_token.update_time
        })


class ResetPassword(AnonymousAPIView):

    @validate(validator=(CaptchaValidation, EmailTokenValidation))
    def post(self, request, data: EmailTokenValidation):
        # step1: 获取注册码对象
        email_token: EmailToken = data.cleaned_data.get('key')

        # step2: 判断验证码类型
        if email_token.mode != 2:
            return self.failed('注册链接已过期，请重新获取')

        # step3: 获取用户
        try:
            user = User.objects.get(email=email_token.email)
        except User.DoesNotExist:
            return self.failed('注册链接已过期，请重新获取')

        # step4: 重置密码
        admin_password_change_form = AdminPasswordChangeForm(user=user, data=request.POST)
        if admin_password_change_form.is_valid():
            admin_password_change_form.save()
        else:
            return self.failed('请求失败!', data={'errors': admin_password_change_form.errors, 'form_errors': True})

        return self.success('密码重置成功！')


class GetImages(UserAPIView, CheckGetPermissionsAPIView):
    """
    获取题目列表
    """

    @validate(GetImagesValidation)
    def get(self, request, data: GetImagesValidation):
        image_queryset = Image.objects.filter(difficulty=data.cleaned_data.get('complexity'),
                                              category=data.cleaned_data.get('category'), status=1)

        image_pagination = CommonPageNumberPagination()
        page_data = image_pagination.paginate_queryset(queryset=image_queryset, request=request, view=self)

        return self.success('获取成功', data={
            'count': image_pagination.page.paginator.count,
            'results': ImagesSerializer(page_data, many=True).data,
        })


class GetImage(UserAPIView, CheckGetPermissionsAPIView):
    """
    获取题目详细
    """

    @validate(IdValidation)
    def get(self, request, data: IdValidation):
        try:
            data = Image.objects.get(id=data.cleaned_data.get('id'), status=1)
        except Image.DoesNotExist:
            return self.failed(msg="题目不存在", status=400)

        return self.success(msg="获取成功", data=ImagesSerializer(data).data)


class RunContainer(UserAPIView, CheckPostPermissionsAPIView):
    """
    启动环境
    """

    @validate(IdValidation)
    def post(self, request, data: IdValidation):

        # 检查是否已经开启了容器
        try:
            container = Container.objects.get(user=request.user)
            return self.success('已存在启动容器！', data={'container': ContainerSerializer(container).data}, code=2)
        except Container.DoesNotExist:
            pass

        try:
            image = Image.objects.get(id=data.cleaned_data.get('id'), status=1)
        except Image.DoesNotExist:
            return self.failed(msg="题目不存在", status=400)

        container = Container()
        container.image = image
        container.user = request.user
        container.save()

        return self.success("启动成功！", data={'container': ContainerSerializer(container).data,
                                           'remaining_time': settings.DOCKER_API.get('AUTO_REMOVE_CONTAINER')})


class GetRunningContainer(UserAPIView, CheckGetPermissionsAPIView):
    """
    获取用户运行中的容器
    """

    def get(self, request):
        try:
            container = Container.objects.get(user=request.user)
            return self.success('获取成功', data={'container': ContainerSerializer(container).data,
                                              'remaining_time': settings.DOCKER_API.get('AUTO_REMOVE_CONTAINER')})
        except Container.DoesNotExist:
            return self.success('获取成功', data={'container': None})


class RemoveContainer(UserAPIView, CheckPostPermissionsAPIView):

    def post(self, request):

        try:
            container = Container.objects.get(user=request.user)

            container.delete()

            return self.success('已成功删除环境')
        except Container.DoesNotExist:
            return self.failed('关闭失败，未找到相应容器', data={'container': None}, code=2)


class CheckFlag(UserAPIView, CheckPostPermissionsAPIView):
    """
    提交 flag
    """

    @validate(FlagValidation)
    def post(self, request, data: FlagValidation):

        try:
            # 获得当前题目
            task = Image.objects.get(id=data.cleaned_data.get('image_id'), status=1)
        except Image.DoesNotExist:
            return self.failed(msg="题目不存在", status=400)

        try:
            # 判断这题是否已经回答过了
            checked = Checked.objects.get(user=request.user, image=task)
            if checked:
                return self.failed('已经回答过啦！进入下一题吧。')
        except Checked.DoesNotExist:
            pass

        # 确定检查方式
        if task.check_flag == 1:
            try:
                container = Container.objects.get(image_id=task.id, user=request.user)
            except Container.DoesNotExist:
                return self.failed('请先启动环境！', status=400)

            if data.cleaned_data.get('flag') != container.flag:
                return self.failed('对不起，你提交的 Flag 不正确。')

        elif task.check_flag == 2:
            if data.cleaned_data.get('flag') != task.file_flag:
                return self.failed('对不起，你提交的 Flag 不正确。')

        else:
            return self.failed('对不起，你提交的 Flag 不正确。')

        # 将任务添加至答题记录代表已完成
        checked = Checked()
        checked.user = request.user
        checked.image = task
        checked.save()

        # 加分
        request.user.point += task.point
        request.user.save()

        return self.success('恭喜你答对了！', data=CheckedSerializer(checked).data)


class GetChecked(UserAPIView, CheckGetPermissionsAPIView):
    """
    分页获取用户答题记录
    """

    def get(self, request):
        checked_pagination = CommonPageNumberPagination(page_size=7)
        checked_queryset = Checked.objects.filter(user=request.user)
        page_data = checked_pagination.paginate_queryset(queryset=checked_queryset, request=request, view=self)

        return self.success('获取成功', data={
            'count': checked_pagination.page.paginator.count,
            'results': CheckedSerializer(page_data, many=True).data,
        })


class Rank(UserAPIView, CheckGetPermissionsAPIView):
    """
    排行榜
    """

    def get(self, request):
        data = User.objects.filter(point__gt=0).order_by('-point')[:7]
        return self.success('获取成功', data={
            'list': UsersSerializer(data, many=True).data
        })
