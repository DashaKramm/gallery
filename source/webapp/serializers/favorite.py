from rest_framework import serializers

from webapp.models.favorite import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'photo', 'album']
