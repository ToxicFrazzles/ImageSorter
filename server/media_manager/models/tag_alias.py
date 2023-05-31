from django.db import models


class TagAlias(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, default="")
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Tag aliases"

    def __str__(self):
        return f"{self.name}"

    def positive_count(self):
        return self.tag.positive_count()

    def negative_count(self):
        return self.tag.negative_count()

    def untagged_count(self):
        return self.tag.untagged_count()

