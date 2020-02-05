from django.db import models
import random
from django.core.validators import RegexValidator
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import pre_save,post_save
#from blissedmaths.utils import unique_otp_generator
from rest_framework.authtoken.models import Token
import os


class UserManager(BaseUserManager):
    def create_user(self,phone,password=None,is_staff=False,is_active=True,is_admin=False):
        if not phone:
            raise ValueError("phone number must be required.")
        elif not password:
            raise ValueError('Password must be required.')
        user_obj=self.model(phone=phone)
        user_obj.set_password(password)
        user_obj.staff=is_staff
        user_obj.active=is_active
        user_obj.admin=is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,phone,password=None):
        user=self.create_user(phone,password=password,is_staff=True)
        return user

    def create_superuser(self,phone,password=None):
        user=self.create_user(phone,password=password,is_staff=True,is_admin=True)
        return user
class UserModel(AbstractBaseUser):
    phone_regx=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number must be entered in the from 9 to 14")
    phone=models.CharField(validators=[phone_regx],max_length=15,unique=True)
    name=models.CharField(max_length=40)
    first_login=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='phone'
    REQUIRED_FIELDS=[]
    objects=UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self,prem,obj=None):
        return True


    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active




class PhoneOtp(models.Model):
    phone_regx=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number must be entered in the from 9 to 14")
    phone=models.CharField(validators=[phone_regx],max_length=15,unique=True)
    otp=models.CharField(max_length=9)
    count=models.IntegerField(default=0,help_text='Number of otp sent.')
    validate_field=models.BooleanField(default=False)


    def __str__(self):
        return self.otp+" is sent to "+ self.phone
