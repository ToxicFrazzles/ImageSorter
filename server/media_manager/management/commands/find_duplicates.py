import numpy as np
from django.core.management.base import BaseCommand, CommandError
from media_manager.models import SourceDirectory, MediaFile, MediaTypeChoices, Setting
from pathlib import Path
from django.db.utils import OperationalError
from PIL import Image, UnidentifiedImageError
from time import sleep
from imagehash import dhash


def is_animated(image):
    try:
        image.seek(1)
        return True
    except EOFError:
        return False


class Command(BaseCommand):
    help = 'Browses each source directory looking for images to add to the database'

    def add_arguments(self, parser):
        parser.add_argument("--once", action='store_true', help='Index all active source directories once instead of repeatedly')

    def handle(self, *args, **options):
        while True:
            print("Searching for duplicates")
            try:
                for media_file in MediaFile.objects.filter(similar_to=None, media_type=0, diff_hash1=None, diff_hash2=None, diff_hash3=None, diff_hash4=None):
                    try:
                        image = Image.open(media_file.file_path)
                    except (UnidentifiedImageError, Image.DecompressionBombError):
                        continue
                    try:
                        raw_im_hash = dhash(image, hash_size=16)
                    except OSError:
                        print(f"{media_file.file_path} is invalid. Possible to recover manually?")
                        continue
                    im_hash = np.packbits(np.array(raw_im_hash.hash).reshape(1, 16**2), axis=1).view(np.int64)[0]

                    similar_images = MediaFile.objects.filter(media_type=0, diff_hash1=im_hash[0], diff_hash2=im_hash[1], diff_hash3=im_hash[2], diff_hash4=im_hash[3])

                    image_arr = np.array(image)
                    should_save = True
                    for similar_image in similar_images:
                        similar_img = Image.open(similar_image.file_path)
                        similar_img_arr = np.array(similar_img)
                        same = np.array_equal(image_arr, similar_img_arr)
                        if same and not is_animated(image) and not is_animated(similar_img):
                            should_save = False
                            Path(media_file.file_path).unlink()
                            media_file.delete()
                            break
                        elif same and is_animated(image) and not is_animated(similar_img):
                            Path(similar_image.file_path).unlink()
                            similar_image.delete()
                            break
                        elif same and not is_animated(image) and is_animated(similar_img):
                            should_save = False
                            Path(media_file.file_path).unlink()
                            media_file.delete()
                        else:
                            media_file.similar_to.add(similar_image)
                    if not should_save:
                        continue
                    media_file.diff_hash1 = im_hash[0]
                    media_file.diff_hash2 = im_hash[1]
                    media_file.diff_hash3 = im_hash[2]
                    media_file.diff_hash4 = im_hash[3]
                    media_file.save()
                if options['once']:
                    print("Done!")
                    break
            except OperationalError:
                sleep(5)
                continue
            print("Sleeping. Zzzzzz")
            sleep(120)
