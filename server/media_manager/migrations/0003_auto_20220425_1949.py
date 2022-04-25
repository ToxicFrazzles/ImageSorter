from django.db import migrations
from pathlib import Path


def add_settings(apps, schema_editor):
    defaults = [
        ('x_accel', 'Use X-Accel-Redirect to serve media', "False")
    ]
    Setting = apps.get_model('media_manager', 'Setting')
    for default in defaults:
        setting, created = Setting.objects.get_or_create(key=default[0], name=default[1], value=default[2])
        if created:
            setting.save()


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0002_mediafile_diff_hash1_mediafile_diff_hash2_and_more'),
    ]

    operations = [
        migrations.RunPython(add_settings),
    ]
