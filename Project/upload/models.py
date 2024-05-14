from django.db import models
from django.contrib.auth.models import User

class MediaFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        # Check if uploaded file is an image
        return self.file.name.endswith('.jpg') or self.file.name.endswith('.jpeg') or self.file.name.endswith('.png')

    def __str__(self):
        return self.file.name
