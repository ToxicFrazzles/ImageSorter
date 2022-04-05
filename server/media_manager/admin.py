from django.contrib import admin
from .models import MediaFile, SourceDirectory, TagGroup, Tag, Setting
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


@admin.register(TagGroup)
class TagGroupAdmin(admin.ModelAdmin):
    actions = ("silently_delete", "clear_group")

    def silently_delete(self, request, queryset):
        queryset.delete()

    def clear_group(self, request, queryset):
        MediaFile.objects.filter(tags__group__in=queryset).delete()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    actions = ("silently_delete",)

    def silently_delete(self, request, queryset):
        queryset.delete()

    def clear_tag(self, request, queryset):
        MediaFile.objects.filter(tags__in=queryset).delete()


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    fields = ('key', 'value')
    readonly_fields = ('name', 'key')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
