from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status


# serializadores para el listado y obtencion de usuarios
from .serializers import UserListSerializer, CustomUserListSerializer
from .serializers import UserRelatedListSerializer

# serializadores para la creacion de usuarios
from .serializers import UserSerializer, CustomUserSerializer

# serializadores para la actualizacion de usuarios
from .serializers import UserUpdateSerializer, CustomUserUpdateSerializer

from django.contrib.auth.models import User
from apps.user.models import CustomUser

"""
Vista basada en clase GenericViewSet para el listado, obtencion, crecion, actualizacion y eliminacion de producto

Se utiliza el decorador action para definir funciones como acciones personalizadas en el ViewSet
Al agregar 'raise_exception=True', lanza una excepción si se produce un error de validación

list: Obtiene una lista de usuarios activos
create: Crea un nuevo CustomUser relacionado con un usuario existente
retrieve: obtiene instancia de CustomUser
destroy: obtiene instancia de CustomUser y hace eliminacion logica accediendo a relacion user
update: obtiene instancia de CustomUser y hace actualiza tanto CustomUser y User

"""


class UserViewSet(GenericViewSet):
    model = CustomUser
    serializer_class = CustomUserListSerializer

    def get_queryset(self):
        # La notación __ en Django se utiliza para realizar búsquedas o consultas a través de relaciones entre modelos
        return self.model.objects.filter(user__is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

        serializer = self.get_serializer(custom_user)

        return Response({"message": "customuser created successfully", "user": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            instance.user.is_active = False
            instance.user.save()
            return Response({'message': 'user deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):

        # Actualiza un objeto User junto con su objeto CustomUser relacionado. Requiere datos actualizados para ambos objetos en 'user_data' y 'custom_user_data' respectivamente.

        instance = self.get_object()
        user_data = request.data.get('user_data', {})
        custom_user_data = request.data.get('custom_user_data', {})

        # Accede al objeto User relacionado
        user_serializer = UserUpdateSerializer(
            instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        customuser_serializer = CustomUserUpdateSerializer(
            instance, data=custom_user_data, partial=True)
        customuser_serializer.is_valid(raise_exception=True)
        customuser = customuser_serializer.save()

        serializer = CustomUserListSerializer(customuser)

        return Response(serializer.data, status=status.HTTP_200_OK)
