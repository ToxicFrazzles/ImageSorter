from django.core.management.base import BaseCommand, CommandError
from image_sorter.models import SourceDirectory, Image as ImageModel
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from time import sleep


class Command(BaseCommand):
    help = 'Browses each source directory looking for images to add to the database'

    def handle(self, *args, **options):
        while True:
            source_directories = SourceDirectory.objects.filter(active=True)
            for dir in source_directories:
                dir_path = Path(dir.file_path).resolve()
                if not dir_path.is_dir():
                    dir.active = False
                    dir.save()
                    continue
                for entity in dir_path.iterdir():
                    if not entity.is_file():
                        continue
                    if ImageModel.objects.filter(file_path=f"{entity}").first() is not None:
                        continue
                    try:
                        img = Image.open(entity)
                    except UnidentifiedImageError:
                        continue
                    image = ImageModel(file_path=f"{entity}")
                    try:
                        image.save()
                    except Exception as e:
                        print(e)
            sleep(120)
