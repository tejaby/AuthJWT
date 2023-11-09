from django.urls import path

from apps.user.api.routers import router

urlpatterns = [

]

urlpatterns += router.urls
