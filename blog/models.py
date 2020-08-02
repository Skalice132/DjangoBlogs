from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import admin


class Tag(models.Model):
        name = models.CharField(max_length=100, verbose_name='Тег')

        class Meta:
                verbose_name = 'Тег'
                verbose_name_plural = 'Теги'

        def __str__(self):
                return f'{self.name}'


class Post(models.Model):
        title = models.CharField(max_length=100, verbose_name='Заголовок',
                                 help_text='Введите заголовок своего поста.')
        text = models.TextField(verbose_name='Текст записи',
                                 help_text='Введите текст своего поста.')
        date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
        author = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   verbose_name='Автор публикации')
        tags = models.ForeignKey(Tag,
                                 on_delete=models.CASCADE,
                                 verbose_name='Тег',
                                 help_text='Выберете тег для удобного поиска.')

        def get_absolute_url(self):
                return reverse('news-detail', kwargs={'pk': self.pk})

        class Meta:
                verbose_name = 'Статья'
                verbose_name_plural = 'Статьи'

        def __str__(self):
                return f'Статья: {self.title}'

        def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
                super().save(force_insert, force_update, using, update_fields)
