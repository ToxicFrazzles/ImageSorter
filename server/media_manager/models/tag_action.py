from django.db import models


class TagAction(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    media_file = models.ForeignKey('MediaFile', on_delete=models.CASCADE)
    human_tagged = models.BooleanField()
    tagged_date = models.DateTimeField(auto_created=True)
    certainty = models.DecimalField(max_digits=6, decimal_places=3)
