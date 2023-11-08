from django.db import models
from django.contrib.auth.models import User


"""
Modelo para un usuario personalizado que extiende el modelo User de Django.

almacena información adicional del usuario, biografía, sitio web, foto de perfil y la fecha de nacimiento.
el atributo auto_now en DateField hara que se actualize automáticamente en cada creación o modificación del objeto
el atributo auto_now_add establecera fecha y hora actual al crear el objeto, pero no se actualizará

"""


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=150, blank=True, null=True)
    website = models.CharField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Usuario personalizado'
        verbose_name_plural = 'Usuarios personalizados'
        ordering = ['user']

    def __str__(self):
        return self.user.username



# Acceder al usuario desde un objeto CustomUser
# Suponiendo que tienes una instancia de CustomUser llamada "custom_user"
    # user = custom_user.user  # Accede al usuario relacionado

# Acceder al objeto CustomUser relacionado desde un objeto User
# Suponiendo que tienes una instancia de User llamada "user"
    # custom_user = user.customuser  # Accede al usuario personalizado relacionado

# acceder a las propiedades de CustomUser y User a través de una consulta utilizando select_related()
# Realiza una consulta que recupere un objeto CustomUser y su objeto User asociado usando select_related
# No se necesita instancia ya sea de CustomUser o User
    # custom_user_query = CustomUser.objects.select_related('user').get(id=1)
