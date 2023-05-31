from django.db import models


class TrainingTask(models.Model):
    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE)
    model = models.ForeignKey('Model', on_delete=models.SET_NULL, null=True, default=None)
    assigned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
