from rest_framework import serializers

from django.contrib.auth.models import User


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
