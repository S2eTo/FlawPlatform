import threading

from django import forms
from django.contrib import admin

from dockerapi.api import docker_api
from dockerapi.models import Image, Container, Checked


class ContainerCreationForm(forms.ModelForm):

    class Meta:
        model = Container
        fields = ("image", )


class ContainerChangeForm(forms.ModelForm):

    class Meta:
        model = Container
        fields = ('image', 'container_id', 'name', 'public_port', 'user')


def post_delete_selected(queryset):
    """
    后台执行批量删除动作后，删除容器
    """

    pass


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    add_form = ContainerCreationForm
    change_form = ContainerChangeForm

    autocomplete_fields = ('image', )
    list_display = ('container_id', 'public_port', 'image', 'user', 'create_time', 'update_time')
    list_filter = ('create_time', 'update_time')
    search_fields = ('container_id', 'image__image_id', 'user__username', 'image__name')
    list_per_page = 10

    def delete_queryset(self, request, queryset):
        """
        兼容删除动作, 删除同时将容器删除
        """

        # 删除容器
        def threading_delete():
            for container in queryset:
                container.is_delete = True
                docker_api.delete(container_id=container.container_id, job_id=container.job_id)

        threading.Thread(target=threading_delete).start()

        # 执行原生删除
        super().delete_queryset(request, queryset)

    def save_model(self, request, obj, form, change):
        """
        后台保存的时候, 自动填充用户名
        """

        if not change:
            obj.user = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        """
        在容器创建时，使用自定义表单
        """

        defaults = {}
        if obj is None:
            self.readonly_fields = ()
            defaults['form'] = self.add_form
        else:
            self.readonly_fields = ('image', 'container_id', 'name', 'public_port', 'user', 'create_time',
                                    'update_time')
            defaults['form'] = self.change_form

        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def has_change_permission(self, request, obj=None):
        """
        不给修改权限
        """

        return False


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    add_form_template = 'admin/image_add_form.html'
    change_form_template = 'admin/image_add_form.html'

    fieldsets = (
        ('环境选择', {'classes': ('dev',), 'fields': ('check_flag',)}),
        ('镜像环境', {'classes': ('image_dev',), 'fields': ('image_id', 'image_tags', 'expose')}),
        ('镜像 FLAG 样式', {'classes': ('flag_style',), 'fields': ('image_flag_style',
                                                               'flag_file_path', 'flag_file_format')}),
        ('附件环境', {'classes': ('file_dev',), 'fields': ('file', 'file_flag')}),
        ('题目信息', {'classes': ('info',),
                  'fields': ('name', 'source', 'difficulty', 'point', 'category', 'status', 'description')}),
    )

    list_editable = ('status', )
    list_display = ('name', 'status', 'check_flag', 'point', 'source', 'difficulty', 'category')
    list_filter = ('difficulty', 'check_flag', 'category', 'status', 'create_time', 'update_time')
    search_fields = ('name', 'image_id', 'description', 'source')
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            self.readonly_fields = ()
        else:
            self.readonly_fields = ('create_time', 'update_time')
        return self.readonly_fields


@admin.register(Checked)
class CheckedAdmin(admin.ModelAdmin):

    list_display = ('user', 'image', 'create_time')
    list_filter = ('create_time', )
    search_fields = ('user_username', 'image__image_name')
    readonly_fields = ('user', 'image')
    list_per_page = 10

    def has_add_permission(self, request):
        """
        不给后台添加权限
        """

        return False

    def has_change_permission(self, request, obj=None):
        """
        不给后台修改权限
        """

        return False
