from django.db import models
from django.contrib.auth.models import User

class MediaFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        return self.file.name.lower().endswith(('.jpg', '.jpeg', '.png'))

    @property
    def is_video(self):
        return self.file.name.lower().endswith(('.mp4'))

    def __str__(self):
        return self.file.name
