from django.db import models


class TagGroup(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, default="")
    parent_tags = models.ManyToManyField('Tag', blank=True, default=None)

    def __str__(self):
        return f"{self.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.parent_tags is not None:
            if self.parent_tags.contains(self):
                self.parent_tags.remove(self)
        super().save(force_insert, force_update, using, update_fields)
