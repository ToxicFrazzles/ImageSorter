from django.contrib import admin
from .models import MediaFile, SourceDirectory, Tag, TagAction, TagAlias
from django.utils.html import mark_safe
from django.urls import reverse


@admin.register(MediaFile)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'URL')

    def URL(self, instance):
        return mark_safe(f"<a href='{reverse('media_manager:media', args=(instance,))}'>Link</a>")


@admin.register(SourceDirectory)
class SourceDirectoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    actions = ("silently_delete",)

    def silently_delete(self, request, queryset):
        queryset.delete()

    def clear_tag(self, request, queryset):
        MediaFile.objects.filter(tags__in=queryset).delete()


@admin.register(TagAlias)
class TagAliasAdmin(admin.ModelAdmin):
    pass


@admin.register(TagAction)
class TagActionAdmin(admin.ModelAdmin):
    pass
