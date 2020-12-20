from django.db import models
from django.contrib.auth.models import AbstractUser


#  I added new features to Django's user model by using the AbstractUser model. Job and Age.
class AddUser(AbstractUser):
    job = models.CharField(max_length=255)
    age = models.CharField(max_length=5)

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

