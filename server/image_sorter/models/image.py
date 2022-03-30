from django.db import models


class Image(models.Model):
    file_path = models.CharField(max_length=100, db_index=True, unique=True)
    tags = models.ManyToManyField("Tag", blank=True)
