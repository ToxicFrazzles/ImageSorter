from django.db import models


class TagGroup(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.name}"
