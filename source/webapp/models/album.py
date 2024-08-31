from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from webapp.models import BaseModel


class Album(BaseModel):
    title = models.CharField(max_length=70, verbose_name='Название')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='Описание')
    author = models.ForeignKey(
        get_user_model(),
        related_name='author_albums',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Автор')
    is_private = models.BooleanField(default=False, verbose_name='Приватный')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('webapp:detail_album', kwargs={'pk': self.pk})

    def clean(self):
        super().clean()
        if self.pk:
            old_is_private = Album.objects.get(pk=self.pk).is_private
            if old_is_private != self.is_private:
                if self.is_private:
                    self.album_photos.update(is_private=True)

    class Meta:
        db_table = 'albums'
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
