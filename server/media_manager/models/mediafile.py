from django.db import models
from pathlib import Path
from .tag_action import TagAction
from .tag import Tag


class MediaTypeChoices(models.IntegerChoices):
    UNKNOWN = -1
    IMAGE = 0
    VIDEO = 1


class MediaFile(models.Model):
    file_path = models.CharField(max_length=200, db_index=True, unique=True)
    tags = models.ManyToManyField("Tag", blank=True, through='TagAction')
    mime_type = models.CharField(max_length=20)
    media_type = models.IntegerField(choices=MediaTypeChoices.choices)

    def path(self) -> Path:
        return Path(self.file_path)
