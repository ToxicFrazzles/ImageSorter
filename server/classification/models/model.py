import os.path

from django.db import models
from django.dispatch import receiver

file_fields = ["tf_model", "tflite_model", "edgetpu_model"]


class Model(models.Model):
    template = models.ForeignKey('Template', on_delete=models.CASCADE)
    tf_model = models.FileField()
    tflite_model = models.FileField(null=True, default=None)
    edgetpu_model = models.FileField(null=True, default=None)
    accuracy = models.DecimalField(null=True, default=None)
    active = models.BooleanField(default=True)


@receiver(models.signals.post_delete, sender=Model)
def auto_delete_file_on_delete(sender, instance: Model, **kwargs):
    """
    Deletes files from filesystem when
    corresponding "Model" object is deleted.
    """
    for field_name in file_fields:
        field = getattr(instance, field_name, None)
        field.delete(save=False)
        # if field and os.path.isfile(field.path):
        #     os.remove(field.path)


@receiver(models.signals.pre_save, sender=Model)
def auto_delete_file_on_change(sender, instance: Model, **kwargs):
    """
    Deletes old file from filesystem when
    corresponding "Model" object is updated with new file.
    """
    if not instance.pk:
        return

    for field_name in file_fields:
        try:
            old_file = getattr(Model.objects.get(pk=instance.pk), field_name)
        except Model.DoesNotExist:
            continue

        new_file = getattr(instance, field_name)
        if not old_file == new_file and os.path.isfile(old_file.path):
            old_file.delete(save=False)
            # os.remove(old_file.path)
