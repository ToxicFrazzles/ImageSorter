from django.contrib import admin
from .models import Tagger


@admin.register(Tagger)
class TaggerAdmin(admin.ModelAdmin):
    pass

