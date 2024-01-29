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

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return f'{self.sender} to {self.receiver} - {self.timestamp}'
    def get_receiver_profile(self):
        # Lấy đối tượng Profile của người nhận tin nhắn
        try:
            receiver_profile = Profile.objects.get(user=self.receiver)
            return receiver_profile
        except Profile.DoesNotExist:
            return None

    def get_receiver_name(self):
        receiver_profile = self.get_receiver_profile()
        if receiver_profile:
            return f"{receiver_profile.first_name} {receiver_profile.last_name}"
        else:
            return None

    def get_receiver_image_url(self):
        receiver_profile = self.get_receiver_profile()
        if receiver_profile and receiver_profile.image:
            return receiver_profile.image.url
        else:
            return None
  
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# #danh sach loi moi ket ban
class FriendInvitation(models.Model):
    sender = models.ForeignKey(User, related_name='sent_invitations', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_invitations', on_delete=models.CASCADE)
    # status = models.CharField(max_length=20,choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    current_time = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} (sent at {self.sent_at})"

#danh sach ban be
class Friendship(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='friend_list')
    friends = models.ManyToManyField(User, related_name='friends')
    current_time = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"Friend List of {self.user.username} (created at {self.current_time})"

#danh sach chap nhan ket bạn
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    current_time = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({'Accepted' if self.accepted else 'Pending'}) (created at {self.created_at})"
