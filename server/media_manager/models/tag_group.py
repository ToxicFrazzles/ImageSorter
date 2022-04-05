from django.db import models


class TagGroup(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, default="")
    parent_tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.parent_tag is not None:
            if self.parent_tag.group.id == self.id:
                self.parent_tag = None
        super().save(force_insert, force_update, using, update_fields)
