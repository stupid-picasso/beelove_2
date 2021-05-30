from datetime import date


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from django.dispatch import receiver


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'


def get_default_profile_image():
    return 'beelove_pics/dummy.png'


class users(AbstractBaseUser):
    userId = models.AutoField(primary_key=True,unique=True)
    FirstName = models.CharField(max_length=30, null=True)
    LastName = models.CharField(max_length=30, null=True)
    Address = models.CharField(max_length=30, null=True)
    City = models.CharField(max_length=30, null=True)
    PostalCode = models.IntegerField(max_length=6,default=0)
    Country = models.CharField(max_length=30, null=True)
    DOB = models.DateField(null=True,default=None)
    PostalCode = models.IntegerField(null=True)
    sex = models.CharField(max_length=6, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_loggedin = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)
    about_me = models.TextField(default='About Me...')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    class Meta:
        app_label = "profiles"

    def __str__(self):
        return str(self.userId)

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class Questiones(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = "profiles"


class questionnaire(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(users, on_delete=models.CASCADE, related_name="questionnaire_user", null=True, blank=True,unique=True)
    question1 = models.CharField(max_length=30,null=True)
    question2 = models.CharField(max_length=30,null=True)
    question3 = models.CharField(max_length=30,null=True)
    question4 = models.CharField(max_length=30,null=True)
    question5 = models.CharField(max_length=30,null=True)
    question6 = models.CharField(max_length=30,null=True)
    question7 = models.CharField(max_length=30,null=True)
    is_deleted=models.BooleanField(default=False)

    class Meta:
        app_label = "profiles"


# class matches(models.Model):
#
#     matchId = models.AutoField(primary_key=True)
#     user1 = models.ForeignKey(users, on_delete=models.CASCADE, related_name="matches_user1", null=True, blank=True)
#     user2 = models.ForeignKey(users, on_delete=models.CASCADE, related_name="matches_user2", null=True, blank=True)
#     is_deleted = models.BooleanField(default=False)
#
#     class Meta:
#         app_label = "profiles"
