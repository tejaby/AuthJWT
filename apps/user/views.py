from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response


from rest_framework_simplejwt.views import TokenObtainPairView

# serializadores para el listado y obtencion de usuarios
from apps.user.api.serializers import CustomUserListSerializer

from apps.user.api.serializers import CustomTokenObtainPairSerializer

'''
Vista basada en clase TokenObtainPairView para la autenticacion de usuarios y creacion de tokens con simplejwt

- Utiliza el serializador que proporciona la clase TokenObtainPairView para validar el usuario y generar tokens.

'''


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        if not request.data.get('username') or not request.data.get('password'):
            return Response({'errors': 'username and password are required'})

        user = authenticate(request=request, username=request.data.get(
            'username'), password=request.data.get('password'))

        if user is None:
            return Response({'errors': 'No se encontró ninguna cuenta activa con las credenciales proporcionadas'})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_serializer = CustomUserListSerializer(user.customuser)

        return Response({'message': 'inicio de sesión exitosamente', 'token': serializer.validated_data, 'user': user_serializer.data}, status=status.HTTP_200_OK)
