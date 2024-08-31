from django.contrib.auth import get_user_model
from django.db import models

from webapp.models import BaseModel


class Album(BaseModel):
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    author = models.ForeignKey(
        get_user_model(),
        related_name='author_albums',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Автор')
    is_private = models.BooleanField(default=False, verbose_name='Статус')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'albums'
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
