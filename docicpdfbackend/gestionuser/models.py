from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

class Role(models.TextChoices):
    PATIENT = 'PAT', 'Patient'
    ADMINISTRATEUR = 'ADM', 'Administrateur'

class UserManager(BaseUserManager):

    def create_user(self, username, email, role=Role.PATIENT, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email), role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')
        if email is None:
            raise TypeError('Users should have a username')
        user = self.create_user(username, email, Role.ADMINISTRATEUR, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    role = models.CharField(max_length=3, choices=Role.choices, default=Role.PATIENT)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_users')

    groups = models.ManyToManyField(Group, related_name='gestionuser_users')
    user_permissions = models.ManyToManyField(Permission, related_name='gestionuser_users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
