from django.contrib.auth import get_user_model
from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='favorites',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Пользователь')
    photo = models.ForeignKey(
        'webapp.Photo',
        related_name='favorite_photos',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Избранные фото')
    album = models.ForeignKey(
        'webapp.Album',
        related_name='favorite_albums',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Избранные альбомы')

    class Meta:
        db_table = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
