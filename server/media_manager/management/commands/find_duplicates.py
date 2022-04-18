import numpy as np
from django.core.management.base import BaseCommand, CommandError
from media_manager.models import SourceDirectory, MediaFile, MediaTypeChoices, Setting
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from time import sleep
from imagehash import dhash


class Command(BaseCommand):
    help = 'Browses each source directory looking for images to add to the database'

    def add_arguments(self, parser):
        parser.add_argument("--once", action='store_true', help='Index all active source directories once instead of repeatedly')

    def handle(self, *args, **options):
        while True:
            print("Searching for duplicates")
            for media_file in MediaFile.objects.filter(similar_to=None, media_type=0, diff_hash1=None, diff_hash2=None, diff_hash3=None, diff_hash4=None):
                image = Image.open(media_file.file_path)
                raw_im_hash = dhash(image, hash_size=16)
                im_hash = np.packbits(np.array(raw_im_hash.hash).reshape(1, 16**2), axis=1).view(np.int64)[0]

                similar_images = MediaFile.objects.filter(media_type=0, diff_hash1=im_hash[0], diff_hash2=im_hash[1], diff_hash3=im_hash[2], diff_hash4=im_hash[3])

                for similar_image in similar_images:
                    media_file.similar_to.add(similar_image)

                media_file.diff_hash1 = im_hash[0]
                media_file.diff_hash2 = im_hash[1]
                media_file.diff_hash3 = im_hash[2]
                media_file.diff_hash4 = im_hash[3]
                media_file.save()
            if options['once']:
                print("Done!")
                break
            print("Sleeping. Zzzzzz")
            sleep(120)
