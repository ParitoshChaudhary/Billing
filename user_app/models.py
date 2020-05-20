from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

# Create your models here.
class RestrauntManager(BaseUserManager):
    def create_user(self, email, username, phone, restraunt_name, password=None, commit=True):
        if not email:
            raise ValueError('Email is required')

        if not username:
            raise ValueError('Username is required')

        if not phone:
            raise ValueError('Phone is required')

        if not restraunt_name:
            raise ValueError('Restraunt name is required')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            phone = phone,
            restraunt_name = restraunt_name,
        )
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, restraunt_name, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            phone = phone,
            restraunt_name = restraunt_name,
            commit=False,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Restraunt(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.CharField(verbose_name='username', unique=True, max_length=25)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    phone = models.CharField(verbose_name='phone number', max_length=13)
    restraunt_name = models.CharField(verbose_name='restraunt name', max_length=60)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'restraunt_name',]

    objects = RestrauntManager()

    def __str__(self):
        return self.restraunt_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Profile(models.Model):
    user = models.OneToOneField(Restraunt, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Profile Pics', default='default.png', null=True)
    address = models.CharField(verbose_name='address', max_length=150, null=True)
    manager_name = models.CharField(verbose_name='manager', max_length=50, null=True)
    state_gst = models.IntegerField(verbose_name='SGST', null=True)
    centre_gst = models.IntegerField(verbose_name='CGST', null=True)
    
    def __str__(self):
        return f'{self.user.restraunt_name} Profile'


class UserRestrauntManager(models.Model):
    User = get_user_model()
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone = models.IntegerField(max_length=13, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
