from django.db import models
from pathlib import Path


class MediaTypeChoices(models.IntegerChoices):
    UNKNOWN = -1
    IMAGE = 0
    VIDEO = 1


class MediaFile(models.Model):
    file_path = models.CharField(max_length=100, db_index=True, unique=True)
    tags = models.ManyToManyField("Tag", blank=True)
    mime_type = models.CharField(max_length=20)
    media_type = models.IntegerField(choices=MediaTypeChoices.choices)

    def path(self) -> Path:
        return Path(self.file_path)
