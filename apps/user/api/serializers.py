from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

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

Este serializador se utiliza para representar los datos de usuarios con detalles específicos del modelo CustomUser

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
            "biography": instance.biography if instance.biography else '',
            "website": instance.website if instance.website else '',
            "profile_picture": instance.profile_picture.url if instance.profile_picture else '',
            "birthdate": instance.birthdate if instance.birthdate else '',
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


# Se agrega un campo custom_user en el serializador UserListSerializer que utiliza el serializaor CustomUserSerializer y usa source='customuser' para indicar que se debe obtener la información de CustomUser a través del campo customuser de User

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
            # Agregamos los datos de custom_user_data al diccionario data, lo que incluye todos los campos de custom_user
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


"""
Serializer para la autenticacion para el inicio de sesion.

validate: Valida las credenciales del usuario y genera un token de acceso
get_token: Genera tokens de actualización y acceso para el usuario autenticado

- la clase RefreshToken se utiliza para crear tokens de actualización y valida los tokens existentes

Crear un token de actualización para un usuario
refresh = RefreshToken.for_user(user)

Crear un nuevo token de acceso usando un token de actualización
refresh = RefreshToken(token)
new_access_token = str(refresh.access_token)


"""


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get(
                'request'), username=username, password=password)

            if not user:
                msg = 'No se encontró un usuario con estas credenciales.'
                # Raises: serializers.ValidationError: Si las credenciales son inválidas o faltan.
                raise serializers.ValidationError(
                    {'error': msg}, code='authorization')
        else:
            msg = 'Debe proporcionar un username y una contraseña.'
            raise serializers.ValidationError(msg, code='authorization')

        data['token'] = self.get_token(user)
        # Returns: dict: Datos validados con token de acceso.
        return data

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return token
