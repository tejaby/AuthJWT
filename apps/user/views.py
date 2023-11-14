from django.contrib.auth import authenticate

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
            return Response({'errors': 'no se encontró ninguna cuenta activa con las credenciales proporcionadas'})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_serializer = CustomUserListSerializer(user.customuser)

        return Response({'message': 'inicio de sesión exitosamente', 'token': serializer.validated_data, 'user': user_serializer.data}, status=status.HTTP_200_OK)


'''
Vista basada en clase TokenRefreshView para la actualización de tokens de acceso.

TokenRefreshView se encarga de aceptar tokens de refresco válidos y generar nuevos tokens de acceso si el token de refresco proporcionado es válido y no está vencido

'''


class CustomTokenRefreshView(TokenRefreshView):
    pass


'''
Vista basada en clase GenericAPIView para la validación del usuario y revocación del token de refresco.


'''


class CustomLogoutPairView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')
        if refresh is None:
            return Response({'errors': 'se requiere el token de actualización'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intenta revocar el token de refresco
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"message": "cierre de sesión exitoso"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"errors": "Token de refresco inválido"}, status=status.HTTP_400_BAD_REQUEST)
