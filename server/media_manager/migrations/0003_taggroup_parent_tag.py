# Generated by Django 4.0.3 on 2022-04-05 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0002_mediafile_media_type_mediafile_mime_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='taggroup',
            name='parent_tag',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media_manager.tag'),
        ),
    ]
