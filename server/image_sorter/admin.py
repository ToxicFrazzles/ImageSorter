from django.contrib import admin
from .models import Image, SourceDirectory, TagGroup, Tag
from django.utils.html import mark_safe
from django.urls import reverse


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'URL')

    def URL(self, instance):
        return mark_safe(f"<a href='{reverse('image_sorter:media', args=(instance,))}'>Link</a>")


@admin.register(SourceDirectory)
class SourceDirectoryAdmin(admin.ModelAdmin):
    pass


@admin.register(TagGroup)
class TagGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
