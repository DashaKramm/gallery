from django.contrib.auth import get_user_model
from django.db import models

from webapp.models import BaseModel


class Photo(BaseModel):
    photo = models.ImageField(upload_to='pictures', verbose_name='Фотография')
    caption = models.CharField(max_length=250, verbose_name='Подпись')
    author = models.ForeignKey(
        get_user_model(),
        related_name='author_photos',
        on_delete=models.CASCADE,
        verbose_name='Автор')
    album = models.ForeignKey(
        'webapp.Album',
        related_name='album_photos',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Альбом')
    is_private = models.BooleanField(default=False, verbose_name='Статус')

    def __str__(self):
        return self.caption[:50]

    class Meta:
        db_table = 'photos'
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
