from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joindate = models.DateField(auto_now_add=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_username(self):
        return self.user.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joindate = models.DateField(auto_now_add=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_username(self):
        return self.user.username


