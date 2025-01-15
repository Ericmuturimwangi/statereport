from django.db import models
from django.contrib.auth.models import User

class EncryptedFile(models.Model):
    file = models.FileField(upload_to="files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    encryption_key = models.CharField(max_length=256)
    file_name = models.CharField(max_length=256, blank=True, null=True)


    def __str__(self):
        return self.file_name
    

class Profile(models.Model):

    ROLE_CHOICES = [
        ('sender', 'Sender'),
        ('receiver', 'Receiver'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    