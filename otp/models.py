from django.db import models

# Create your models here.
class UserModel(models.Model):
    phonenumber = models.IntegerField(blank=False,unique=True)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.phonenumber)
