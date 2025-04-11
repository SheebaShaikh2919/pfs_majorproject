from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # You can add custom fields here if needed in the future
    pass

class StyleShirt(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='styles/')  # This will work with Cloudinary if configured

    def __str__(self):
        return self.name
