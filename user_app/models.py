from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class RestrauntManager(BaseUserManager):
    def create_user(self, username, email, phone, restraunt_name,
                    is_staff=False, is_admin=False, is_active=True, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        if not password:
            raise ValueError('User must have a password')
        if not phone:
            raise ValueError('User must have a phone number')
        if not restraunt_name:
            raise ValueError('User must have a restraunt name')

        user = self.model(
                email = self.normalize_email(email),
                username = username,
                phone = phone,
                restraunt_name = restraunt_name
        )
        user.set_password(password)
        user.staff = is_staff
        user.active = is_active
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, phone, restraunt_name, password=None):
        user = self.create_user(
                email = self.normalize_email(email),
                username = username,
                phone = phone,
                restraunt_name = restraunt_name,
                is_staff = True
        )
        return user

    def create_superuser(self, email, username, phone, restraunt_name, password=None):
        user = self.create_user(
                email = self.normalize_email(email),
                username = username,
                phone = phone,
                restraunt_name = restraunt_name,
                password = password,
                is_staff = True,
                is_admin = True
        )
        user.save(using=self._db)
        return user

class Restraunt(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(verbose_name = 'email', max_length=60, unique=True)
    username = models.CharField(verbose_name='username', max_length=30, unique=True)
    # password = models.CharField(verbose_name='password', max_length=32)
    phone = models.CharField(verbose_name='phone', max_length=14)
    manager_name = models.CharField(verbose_name='manager_name', max_length=20)
    restraunt_name = models.CharField(verbose_name='restraunt_name', max_length=35)
    address = models.CharField(verbose_name='address', max_length=150, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'restraunt_name']

    objects = RestrauntManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.manager_name

    def get_short_name(self):
        return self.restraunt_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user an admin?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
