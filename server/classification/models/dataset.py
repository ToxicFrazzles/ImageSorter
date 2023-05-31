from django.db import models


class Dataset(models.Model):
    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    tag_actions = models.ManyToManyField('media_manager.TagAction', default=None, null=True)
    active = models.BooleanField(default=True)
