from django.db import models


class InferenceTask(models.Model):
    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    model = models.ForeignKey('Model', on_delete=models.SET_NULL, null=True, default=None)
    media_file = models.ForeignKey('media_manager.MediaFile', on_delete=models.CASCADE)
    result = models.DecimalField(default=None, null=True)
    assigned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
