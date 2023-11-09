from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserListSerializer
from .serializers import UserListSerializer1
from .serializers import CustomUserListSerializer


from django.contrib.auth.models import User
from apps.user.models import CustomUser


class UserViewSet(GenericViewSet):
    model = CustomUser
    serializer_class = CustomUserListSerializer

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
