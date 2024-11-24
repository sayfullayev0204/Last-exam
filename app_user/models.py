from django.contrib.auth.models import AbstractUser
from django.db import models
from app_user.managers import UserModelManager  , AdminManager , CustomerManager

class UserModel(AbstractUser):
    email = models.EmailField(max_length=55, unique=True)
    first_name = models.CharField(max_length=50, default='Anonymous')
    last_name = models.CharField(max_length=55)
    username = models.CharField(max_length=55, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='user-default.png',
        null=True, blank=True
    )
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    objects = UserModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['id']



class Admin(UserModel):
    objects = AdminManager()

    class Meta:
        proxy = True


# Customer proxy modeli
class Customer(UserModel):
    objects = CustomerManager()

    class Meta:
        proxy = True



