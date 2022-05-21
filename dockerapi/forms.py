from django import forms

from dockerapi.models import Container


class ContainerCreationForm(forms.ModelForm):

    class Meta:
        model = Container
        fields = ("image", )


class ContainerChangeForm(forms.ModelForm):

    class Meta:
        model = Container
        fields = ('image', 'container_id', 'name', 'public_port', 'username', 'create_time',
                  'update_time')
