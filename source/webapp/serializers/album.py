from rest_framework import serializers

from webapp.models.album import Album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'title', 'description', 'created_at', 'author', 'is_private']
        read_only_fields = ['id', 'created_at', 'author']
