from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=155, null=True, blank=True, verbose_name='username')
    email = models.EmailField(unique=True, verbose_name='Email address')
    password = models.CharField(max_length=255, verbose_name='Password')
    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)
    is_blocked = models.BooleanField(default=False, verbose_name='Is blocked')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = [
            ('can_block_user', 'Can block user'),
        ]

    def __str__(self):
        return self.email
