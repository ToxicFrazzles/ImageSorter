import secrets
import string
from django.core.management.base import BaseCommand, CommandError
from ...models import SourceDirectory, MediaFile, MediaTypeChoices
from django.conf import settings
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from time import sleep
import magic
from typing import List
from datetime import datetime
from shortuuid import uuid


class Command(BaseCommand):
    help = 'Browses each source directory looking for images to add to the database'

    def add_arguments(self, parser):
        parser.add_argument("--once", action='store_true', help='Index all active source directories once instead of repeatedly')

    def handle(self, *args, **options):
        media_home_dir = Path(settings.MEDIA_HOME_DIRECTORY).resolve()
        if not media_home_dir.is_dir():
            media_home_dir.mkdir(parents=True)
        while True:
            source_directories = SourceDirectory.objects.filter(active=True)
            print("Scanning...")
            for dir in source_directories:
                if dir.path.is_absolute():
                    dir_path = dir.path
                else:
                    dir.active = False
                    dir.save()
                    continue
                if not dir_path.is_dir():
                    dir.active = False
                    dir.save()
                    continue
                to_search = [dir_path]
                while to_search:
                    cur_dir = to_search.pop()
                    for entity in cur_dir.iterdir():
                        if dir.recursive and entity.is_dir():
                            to_search.append(entity)
                            continue
                        if not entity.is_file():
                            continue
                        mime = magic.from_file(entity, mime=True)
                        media_type_map = {
                            "image": MediaTypeChoices.IMAGE,
                            "video": MediaTypeChoices.VIDEO
                        }
                        media_type = mime.split("/")[0]
                        if media_type not in media_type_map:
                            print(mime)
                            continue
                        new_path = (media_home_dir /
                                    f"{datetime.today().strftime('%Y-%m-%d')}" /
                                    (uuid() + entity.suffix)).resolve()
                        new_path.parent.mkdir(parents=True, exist_ok=True)
                        image = MediaFile(file_path=f"{new_path}", mime_type=mime, media_type=media_type_map[media_type])
                        try:
                            entity.rename(new_path)
                            image.save()
                        except Exception as e:
                            print(e)
            if options['once']:
                break
            print("Sleeping. Zzzzzz")
            sleep(120)
