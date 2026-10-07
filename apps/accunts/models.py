from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.accunts.menegr import CustomUserManager

# Create your models here.

class CostumeUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/',null=True,blank=True , verbose_name='Avatar', help_text='Upload your avatar image.')
    email = models.EmailField(unique=True , verbose_name='Email Address', help_text='Enter a valid email address.')
    password = models.CharField(max_length=128 , verbose_name='Password', help_text='Enter a secure password.')


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'password']

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

    def __str__(self):
        return self.email




