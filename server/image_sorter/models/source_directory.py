from django.db import models


class SourceDirectory(models.Model):
    file_path = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Source Directories"

    def __str__(self):
        return self.file_path
