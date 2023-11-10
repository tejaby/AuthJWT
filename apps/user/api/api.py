from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .serializers import UserListSerializer, CustomUserListSerializer
from .serializers import UserRelatedListSerializer

# serializadores para la creacion de usuarios
from .serializers import UserSerializer, CustomUserSerializer

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
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer_user = self.get_serializer(user)
        return Response({'message': 'user created successfully', 'user': serializer_user.data}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def create_customuser(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customuser = serializer.save()
        customuser_serializer = CustomUserListSerializer(customuser)
        return Response({'message': 'customuser created successfully', 'customuser': customuser_serializer.data}, status=status.HTTP_201_CREATED)
