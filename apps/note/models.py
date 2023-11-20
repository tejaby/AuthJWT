from django.db import models

from apps.base.models import BaseModel
from apps.user.models import User

# Create your models here.


class Note(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return self.title
