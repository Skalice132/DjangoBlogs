from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
        title = models.CharField(max_length=100, verbose_name='Заголовок')
        text = models.TextField(verbose_name='Текст записи')
        date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
        author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор публикации')

        def __str__(self):
                return self.title

        def get_absolute_url(self):
                return reverse('news-detail', kwargs={'pk': self.pk})
