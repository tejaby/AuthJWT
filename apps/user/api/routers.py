from rest_framework.routers import DefaultRouter

from .api import UserViewSet

router = DefaultRouter()

router.register(r'user', UserViewSet, basename='users')