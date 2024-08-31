from rest_framework import serializers

from webapp.models.photo import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'photo', 'caption', 'created_at', 'author', 'album', 'is_private', 'access_token']
        read_only_fields = ['id', 'created_at', 'author', 'access_token']
