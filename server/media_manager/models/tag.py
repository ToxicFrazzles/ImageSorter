from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, default="")#
    group = models.ForeignKey('TagGroup', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
