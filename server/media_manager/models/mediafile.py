from django.db import models
from pathlib import Path
from PIL import Image


class MediaTypeChoices(models.IntegerChoices):
    UNKNOWN = -1
    IMAGE = 0
    VIDEO = 1


class MediaFile(models.Model):
    file_path = models.CharField(max_length=200, db_index=True, unique=True)
    tags = models.ManyToManyField("Tag", blank=True, through='TagAction')
    mime_type = models.CharField(max_length=20)
    media_type = models.IntegerField(choices=MediaTypeChoices.choices)

    x_resolution = models.PositiveIntegerField(default=None, null=True)
    y_resolution = models.PositiveIntegerField(default=None, null=True)

    diff_hash1 = models.BigIntegerField(default=None, null=True)
    diff_hash2 = models.BigIntegerField(default=None, null=True)
    diff_hash3 = models.BigIntegerField(default=None, null=True)
    diff_hash4 = models.BigIntegerField(default=None, null=True)
    similar_to = models.ManyToManyField('MediaFile', default=None, related_name='similar_files')

    def path(self) -> Path:
        return Path(self.file_path)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.media_type == 0 and (self.x_resolution is None or self.y_resolution is None):
            img = Image.open(self.file_path)
            self.x_resolution, self.y_resolution = img.size
        super().save(force_insert, force_update, using, update_fields)
