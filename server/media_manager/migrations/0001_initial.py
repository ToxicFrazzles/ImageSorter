# Generated by Django 4.0.3 on 2022-03-31 19:29

from django.db import migrations, models
import django.db.models.deletion
from pathlib import Path


def add_settings(apps, schema_editor):
    defaults = [
        ('media_home', 'Media Home Directory', Path(__file__).parent.parent.parent / "media_home")
    ]
    Setting = apps.get_model('media_manager', 'Setting')
    for default in defaults:
        setting, created = Setting.objects.get_or_create(key=default[0], name=default[1], value=default[2])
        if created:
            setting.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, db_index=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SourceDirectory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=100)),
                ('recursive', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Source Directories',
            },
        ),
        migrations.CreateModel(
            name='TagGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, default='')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_manager.taggroup')),
            ],
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(db_index=True, max_length=100, unique=True)),
                ('tags', models.ManyToManyField(blank=True, to='media_manager.tag')),
            ],
        ),
        migrations.RunPython(add_settings),
    ]
