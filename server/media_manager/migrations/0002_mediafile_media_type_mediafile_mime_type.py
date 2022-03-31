# Generated by Django 4.0.3 on 2022-03-31 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='media_type',
            field=models.IntegerField(choices=[(-1, 'Unknown'), (0, 'Image'), (1, 'Video')]),
        ),
        migrations.AddField(
            model_name='mediafile',
            name='mime_type',
            field=models.CharField(max_length=20),
        ),
    ]