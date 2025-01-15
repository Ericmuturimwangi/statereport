from django.db import models

class EncryptedFile(models.Model):
    file = models.FileField(upload_to="files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    encryption_key = models.CharField(max_length=256)
    file_name = models.CharField(max_length=256, blank=True, null=True)


    def __str__(self):
        return self.file_name
    
