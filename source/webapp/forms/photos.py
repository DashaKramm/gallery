from django import forms

from webapp.models import Photo, Album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo', 'caption', 'album', 'is_private']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['album'].queryset = Album.objects.filter(author=user)
        else:
            self.fields['album'].queryset = Album.objects.none()
