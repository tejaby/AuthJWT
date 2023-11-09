from rest_framework import serializers

from django.contrib.auth.models import User
from apps.user.models import CustomUser


"""
Serializador para el listado de usuarios.

se utiliza para representar una lista de usuarios en la API
se personaliza la representación de los datos utilizando el método to_representation

"""


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "nombre de usuario": instance.username,
            "correo electrónico": instance.email,
            "nombres": instance.first_name,
            "apellidos": instance.last_name
        }


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('id')

    def to_representation(self, instance):
        return {
            "id": instance.user.id,
            "nombre de usuario": instance.user.username,
            "correo electrónico": instance.user.email,
            "nombres": instance.user.first_name,
            "apellidos": instance.user.last_name,
            "biography": instance.biography,
            "website": instance.website,
            "profile_picture": instance.profile_picture.url if instance.profile_picture else None,
            "birthdate": instance.birthdate,
        }


"""
Serializador para la creacion de usuarios.

se utiliza para crear nuevos usuarios en la API
Se sobrescribe el método create para encriptar la contraseña utilizando el método set_password

"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
