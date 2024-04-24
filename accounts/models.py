from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from services.utils import unique_slugify 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='accounts/default.jpg',
        upload_to='images/profile_images/',
    )
    bio = models.TextField(max_length=900)

    def __str__(self) -> str:
        return self.user.username

    # Function for formatting avatar
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 250 or img.width > 250:
            new_img = (250, 250)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})

        