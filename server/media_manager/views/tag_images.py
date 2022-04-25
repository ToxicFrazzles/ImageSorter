import json
from .login_required import LoginRequiredView
from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.db.models import Count
from django import forms
from ..models import MediaFile, Tag, TagAction


def get_next_image_set(tag: Tag):
    media_set = MediaFile.objects.exclude(tags=tag)
    return media_set.filter(media_type=0).distinct().order_by('?')[:20]


class TagImagesView(LoginRequiredView):
    def get(self, request, tag):
        the_images = get_next_image_set(tag)
        if the_images.count() == 0:
            return redirect('media_manager:tag_list')
        ctx = {
            "the_images": the_images,
            "tag": tag
        }
        return render(request, 'media_manager/tag_images.html', context=ctx)

    def post(self, request, tag: Tag):
        post_data = json.loads(request.body)

        for positive_match in post_data.get('positives'):
            image: MediaFile = MediaFile.objects.select_related().prefetch_related().get(id=positive_match)
            if image.tags.contains(tag):
                # Image already tagged for this tag group.
                # Remove the tag so it can be replaced
                TagAction.objects.get(media_file=image).delete()
            image.tags.add(tag,
                           through_defaults={'certainty': 50, 'human_tagged': True, 'positive': True})
            image.save()

        for negative_match in post_data.get('negatives'):
            image: MediaFile = MediaFile.objects.select_related().prefetch_related().get(id=negative_match)
            if image.tags.contains(tag):
                # Image already tagged for this tag group.
                # Remove the tag so it can be replaced
                TagAction.objects.get(media_file=image).delete()
            image.tags.add(tag,
                           through_defaults={'certainty': 50, 'human_tagged': True, 'positive': False})
            image.save()

        next_images = get_next_image_set(tag)
        return JsonResponse({
            "next_images": [{
                "id": next_image.id,
                "url": reverse("media_manager:media", args=(next_image,)),
                "mime-type": next_image.mime_type,
                "media_type": next_image.media_type,
            } for next_image in next_images]
        })
