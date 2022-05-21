from rest_framework import serializers

from users.models import User
from dockerapi.models import Image, Container, Checked


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'check_flag', 'file', 'name', 'source', 'description', 'point', 'difficulty', 'category']


class ContainerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: Container):
        return {
            "name": obj.image.name,
            "id": obj.image.id
        }

    def get_user(self, obj: Container):
        return obj.user.username

    class Meta:
        model = Container
        fields = ['id', 'container_id', 'name', 'public_port', 'image', 'user', 'create_time']
        depth = 1


class CheckedSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: Checked):
        return {
            "id": obj.image.id,
            "name": obj.image.name,
            "point": obj.image.point,
            "category": obj.image.category,
            "check_flag": obj.image.check_flag,
            "difficulty": obj.image.difficulty,
            "create_time": obj.image.create_time
        }

    class Meta:
        model = Checked
        fields = ['id', 'image', 'create_time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'point', 'avatar', 'email']


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'point', 'date_joined']
