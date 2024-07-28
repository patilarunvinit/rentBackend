from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    b_date = models.DateField(null = True)
    owner_photo = models.ImageField(upload_to='images/', null=True, verbose_name="")
    username = models.CharField(max_length=255, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email