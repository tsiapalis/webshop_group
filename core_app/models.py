from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'