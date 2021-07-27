from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Temporarystorage(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    send_at = models.DateTimeField()

    @property
    def timestampnow(self):
        self.send_at = timezone.now()


# custom user model belongs to blogsAPP.models