from django.db import models
from pathlib import Path


class MediaFile(models.Model):
    file_path = models.CharField(max_length=100, db_index=True, unique=True)
    tags = models.ManyToManyField("Tag", blank=True)

    def path(self) -> Path:
        return Path(self.file_path)
