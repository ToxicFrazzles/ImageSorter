from django.db import models


class Template(models.Model):
    name = models.CharField(max_length=16)
    description = models.TextField(blank=True, default="")
    required_tags = models.ManyToManyField('media_manager.Tag', null=True, default=None)
    tag = models.ForeignKey('media_manager.Tag', on_delete=models.CASCADE)
