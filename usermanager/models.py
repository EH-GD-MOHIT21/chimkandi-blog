from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models
from .model_managers import UserManager
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class Temporarystorage(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    send_at = models.DateTimeField()

    @property
    def timestampnow(self):
        self.send_at = timezone.now()




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    superuser = models.BooleanField(default=False) # a superuser
    

    last_reward_claimed = models.DateField(null=True,blank=True)
    nested_balance = models.FloatField(default=1.0)
    profile_pic = models.ImageField(null=True,blank=True,upload_to='imgs')
    Referal_by = models.EmailField(null=True,blank=True)


    @property
    def reward(self):
        self.last_reward_claimed = timezone.now().date()

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_superuser(self):
        "Is the user a admin member?"
        return self.superuser


    objects = UserManager()