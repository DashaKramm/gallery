from django.contrib import admin

from webapp.models import Photo, Album, Favorite


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption', 'created_at', 'album', 'is_private', 'author']
    list_display_links = ['id', 'caption']
    search_fields = ['caption', 'author__username']
    fields = ['photo', 'caption', 'album', 'is_private']
    list_filter = ['is_private', 'created_at', 'album']
    readonly_fields = ['author', 'created_at']


admin.site.register(Photo, PhotoAdmin)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'created_at', 'is_private', 'author']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'description']
    fields = ['title', 'description', 'is_private']
    list_filter = ['is_private', 'created_at']
    readonly_fields = ['author', 'created_at']


admin.site.register(Album, AlbumAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'photo', 'album']
    list_display_links = ['id', 'user']
    search_fields = ['user__username', 'photo__caption', 'album__title']
    fields = ['user', 'photo', 'album']
    list_filter = ['user', 'photo', 'album']
    readonly_fields = ['user']


admin.site.register(Favorite, FavoriteAdmin)
