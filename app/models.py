from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    session_token = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.session_token}"

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    aboutme = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10,  null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    relationship_status = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
         return f"{self.user.username} - {self.first_name} {self.last_name}"

class ConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=20)
    expiration_date = models.DateTimeField(default=timezone.now() + timedelta(minutes=1))
     # Thay đổi ở đây



  