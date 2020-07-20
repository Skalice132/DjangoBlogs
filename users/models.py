from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Ник')
    img = models.ImageField(default="default.jpg", upload_to='user_images', verbose_name='Загрузить картинку')

    def __str__(self):
        return f'Установить аву {self.user.username}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        image = Image.open(self.img.path)
        if image.height > 64 or image.width > 64:
            resize = (64,64)
            image.thumbnail(resize)
            image.save(self.img.path)
