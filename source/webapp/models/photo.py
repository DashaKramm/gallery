from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

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
    is_private = models.BooleanField(default=False, verbose_name='Приватное')

    def __str__(self):
        return self.caption[:50]

    def get_absolute_url(self):
        return reverse('webapp:detail_photo', kwargs={'pk': self.pk})

    def clean(self):
        if self.album and self.album.author != self.author:
            raise ValidationError("Вы не можете добавлять фотографии в альбомы, которые Вам не принадлежат")
        if self.album and self.album.is_private and not self.is_private:
            raise ValidationError('Фотография не может быть публичной, если альбом приватный')

    class Meta:
        db_table = 'photos'
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
