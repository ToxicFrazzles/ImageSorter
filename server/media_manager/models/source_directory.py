from django.db import models
from pathlib import Path


class SourceDirectory(models.Model):
    file_path = models.CharField(max_length=100)
    recursive = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Source Directories"

    def __str__(self):
        return self.file_path

    @property
    def path(self):
        return Path(self.file_path).resolve()
