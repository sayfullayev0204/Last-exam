from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError


class UserModelManager(UserManager):
    def create_user(self, email: str,
                    first_name: str = None,
                    last_name: str = None,
                    username: str = None,
                    password=None):
        if not email:
            raise ValidationError('Users must have an email address')

        email = self.normalize_email(email=email)

        if not username:
            username = email.split('@')[0]

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
        )
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_customer=True)


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)
