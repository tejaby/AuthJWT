from django.shortcuts import get_object_or_404

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import authentication

from rest_framework_simplejwt import authentication

from .serializers import UserListSerializer, CustomUserListSerializer
from .serializers import UserRelatedListSerializer

# serializadores para la creacion de usuarios
from .serializers import UserSerializer, CustomUserSerializer

# serializadores para la actualizacion de usuarios
from .serializers import UserUpdateSerializer, CustomUserUpdateSerializer

# from .serializers import UserListSerializer1


from django.contrib.auth.models import User
from apps.user.models import CustomUser

"""
Vista basada en clase GenericViewSet para el listado, obtencion, crecion, actualizacion y eliminacion de producto

Se utiliza el decorador action para definir funciones como acciones personalizadas en el ViewSet
Al agregar 'raise_exception=True', lanza una excepción si se produce un error de validación

list: Obtiene una lista de usuarios activos
create: Crea un nuevo usuario
create_customuser: Crea un nuevo CustomUser relacionado con un usuario existente

"""


class UserViewSet(GenericViewSet):
    model = User
    serializer_class = UserRelatedListSerializer

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = CustomUser.objects.all()
        serializer = CustomUserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     serializer_user = self.get_serializer(user)
    #     return Response({'message': 'user created successfully', 'user': serializer_user.data}, status=status.HTTP_201_CREATED)

    # @action(methods=['POST'], detail=False)
    # def create_customuser(self, request, *args, **kwargs):
    #     serializer = CustomUserSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     customuser = serializer.save()
    #     customuser_serializer = CustomUserListSerializer(customuser)
    #     return Response({'message': 'customuser created successfully', 'customuser': customuser_serializer.data}, status=status.HTTP_201_CREATED)

    # def create(self, request, *args, **kwargs):
    #     user = request.data.get('user', {})
    #     serializer = UserSerializer(data=user)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()

    #     customuser = request.data.get('customuser', {})
    #     customuser['user'] = user.id
    #     self.create_customuser(customuser)
    #     custom_serializer = self.get_serializer(user)
    #     return Response(custom_serializer.data, status=status.HTTP_201_CREATED)

    # def create_customuser(self, data):
    #     serializer = CustomUserSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    def create(self, request, *args, **kwargs):
        # Crea un nuevo objeto CustomUser junto con un objeto User relacionado. Requiere datos para ambos objetos en user_data y custom_user_data respectivamente

        user_data = request.data.get('user_data', {})
        custom_user_data = request.data.get('custom_user_data', {})

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        custom_user_data['user'] = user.id

        customuser_serializer = CustomUserSerializer(
            data=custom_user_data)
        customuser_serializer.is_valid(raise_exception=True)
        custom_user = customuser_serializer.save()

        serializer = CustomUserListSerializer(custom_user)

        return Response({"message": "customuser created successfully", "user": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # instance = CustomUser.objects.filter(pk=pk).first()
        instance = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(CustomUser, pk=pk)
        if instance is not None:
            instance.user.is_active = False
            instance.user.save()
            return Response({'message': 'user deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, *args, **kwargs):

        # Actualiza un objeto User junto con su objeto CustomUser relacionado. Requiere datos actualizados para ambos objetos en 'user_data' y 'custom_user_data' respectivamente.

        instance = get_object_or_404(CustomUser, pk=pk)
        user_data = request.data.get('user_data', {})
        custom_user_data = request.data.get('custom_user_data', {})

        user_serializer = UserUpdateSerializer(
            instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Accede al objeto CustomUser relacionado
        # customuser_instance = instance.customuser
        customuser_serializer = CustomUserUpdateSerializer(
            instance, data=custom_user_data, partial=True)
        customuser_serializer.is_valid(raise_exception=True)
        customuser = customuser_serializer.save()

        serializer = CustomUserListSerializer(customuser)

        return Response(serializer.data, status=status.HTTP_200_OK)
