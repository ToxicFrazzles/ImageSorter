from django.db import models


class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name
