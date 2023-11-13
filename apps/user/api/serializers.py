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


"""
Serializador para el listado de usuarios con datos relacionados al modelo CustomUser.

Este serializador se utiliza para representar los datos de usuarios con detalles específicos del modelo CustomUser.

"""


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['id']

    def to_representation(self, instance):
        return {
            "id": instance.id,
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
Otra forma del Serializador para el listado de usuarios con datos relacionados al modelo CustomUser.

para acceder a los campos de customuser en CustomUserRelatedSerializer se anida el  serializador de CustomUser

"""


# Se crea un serializador para CustomUser que muestre los campos que deseas

class CustomUserRelatedSerializer (serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['biography', 'website', 'profile_picture', 'birthdate']


# Se agrega un campo custom_user en el serializador UserListSerializer que utiliza el serializaor CustomUserSerializer y usa source='customuser' para indicar que se debe obtener la información de CustomUser a través del campo customuser de User.

class UserRelatedListSerializer(serializers.ModelSerializer):
    custom_user = CustomUserRelatedSerializer(source='customuser')

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'custom_user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Extraemos los datos del campo custom_user del diccionario data utilizando el método pop.
        custom_user_data = data.pop('custom_user')
        if custom_user_data is not None:
            # Agregamos los datos de custom_user_data al diccionario data, lo que incluye todos los campos de custom_user.
            data.update(custom_user_data)
        return data


"""
Serializador para la creacion de usuarios.

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


"""
Serializador para la creacion de usuarios del modelo CustomUser.

"""


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


"""
Serializador para la actualizacion de usuarios del modelo User.

"""


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


"""
Serializador para la actualizacion de usuarios del modelo CustomUser.

"""


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['biography', 'website', 'birthdate', 'profile_picture']
