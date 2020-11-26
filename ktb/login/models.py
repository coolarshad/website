from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

# from .managers import UserManager
from django.db import models

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, name, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not name:
            raise ValueError('The given name must be set')
        # email = self.normalize_email(email)
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, password, **extra_fields)

    def create_superuser(self, name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	name=models.CharField(max_length=255,unique=True)
	position=models.CharField(max_length=100, blank=True)
	authority=models.CharField(max_length=30, blank=True)
	contact=models.CharField(max_length=100, blank=True)
	email=models.CharField(max_length=100, blank=True)
	password=models.CharField(max_length=100, blank=True)

	objects = UserManager()

	USERNAME_FIELD = 'name'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

    # def get_full_name(self):
    #     '''
    #     Returns the first_name plus the last_name, with a space in between.
    #     '''
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()

    # def get_short_name(self):
    #     '''
    #     Returns the short name for the user.
    #     '''
    #     return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)
# class Users(models.Model):
# 	name=models.CharField(max_length=255)
# 	position=models.CharField(max_length=255)
# 	authority=models.CharField(max_length=255)
# 	contact=models.CharField(max_length=255)
# 	email=models.CharField(max_length=255)
# 	password=models.CharField(max_length=255)
	

# 	def __str__(self):
# 		return self.name
