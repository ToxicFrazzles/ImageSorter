from django.db import models
from .tag_action import TagAction
from .mediafile import MediaFile


class Tag(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.name}"

    def positive_count(self):
        return TagAction.objects.filter(tag=self, positive=True).count()

    def negative_count(self):
        return TagAction.objects.filter(tag=self, positive=False).count()

    def untagged_count(self):
        return MediaFile.objects.filter(media_type=MediaFile.MediaType.IMAGE).count() - TagAction.objects.filter(tag=self).count()
