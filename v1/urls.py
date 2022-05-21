from django.urls import path

from v1.views import (
    Login, GetImages, CheckIn, GetImage, RunContainer, GetRunningContainer, RemoveContainer,
    CheckFlag, GetUserInfo, GetChecked, Avatar, BindEmail, Register, GetCaptcha, Logout,
    GetResetPasswordEmail, ResetPassword, Rank
)


urlpatterns = [
    # 获取验证码: /v1/get_captcha
    path('get_captcha', GetCaptcha.as_view()),

    # 用户注册: /v1/register
    path('register', Register.as_view()),

    # 完成注册: /v1/bind_email
    path('bind_email', BindEmail.as_view()),

    # 登录: /v1/login
    path('login', Login.as_view()),

    # 验证登录: /v1/checkin
    path('checkin', CheckIn.as_view()),

    # 退出登录: /v1/logout
    path('logout', Logout.as_view()),

    # 获取用户信息: /v1/get_userinfo
    path('get_userinfo', GetUserInfo.as_view()),

    # 更换头像: /v1/avatar
    path('avatar', Avatar.as_view()),

    # 获取重置密码邮件: /v1/get_reset_password_email
    path('get_reset_password_email', GetResetPasswordEmail.as_view()),

    # 重置密码: /v1/reset_password
    path('reset_password', ResetPassword.as_view()),

    # 获取题目: /v1/get_image
    path('get_image', GetImages.as_view()),

    # 获取题目详细: /v1/get_image_detail
    path('get_image_detail', GetImage.as_view()),

    # 启动容器: /v1/run_container
    path('run_container', RunContainer.as_view()),

    # 获取当前用户运行的容器: /v1/get_running_container
    path('get_running_container', GetRunningContainer.as_view()),

    # 停止并删除容器: /v1/remove_container
    path('remove_container', RemoveContainer.as_view()),

    # 提交 flag: /v1/check_flag
    path('check_flag', CheckFlag.as_view()),

    # 分页获取答题记录: /v1/get_checked
    path('get_checked', GetChecked.as_view()),

    # 获取排行信息
    path('rank', Rank.as_view()),
]

