from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='users/images', default='users/images/default.png')

    def __str__(self):
        return self.name