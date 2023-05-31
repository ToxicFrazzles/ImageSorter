import json
from .login_required import LoginRequiredView
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http.response import JsonResponse
from django.db.models import Count
from django import forms
from ..models import MediaFile, Tag, TagAction


def get_next_image(tag: Tag):
    media_set = MediaFile.objects.exclude(tags=tag)
    return media_set.distinct().order_by('?').first()


class TagImageView(LoginRequiredView):
    def get(self, request, tag_id):
        tag: Tag = get_object_or_404(Tag, id=tag_id)
        the_image = get_next_image(tag)
        if the_image is None:
            return redirect('media_manager:tag_list')
        ctx = {
            "the_image": the_image,
            "tag": tag
        }
        return render(request, 'media_manager/tag_image.html', context=ctx)

    def post(self, request, tag_id):
        tag: Tag = get_object_or_404(Tag, id=tag_id)
        post_data = json.loads(request.body)
        image: MediaFile = MediaFile.objects.select_related().prefetch_related().get(id=post_data.get("image_id"))
        if image.tags.contains(tag):
            # Image already tagged for this tag group.
            # Remove the tag so it can be replaced
            TagAction.objects.get(media_file=image).delete()
        image.tags.add(tag, through_defaults={'certainty': 50, 'human_tagged': True, 'positive': post_data['positive']})
        image.save()

        next_image = get_next_image(tag)
        return JsonResponse({
            "next_image": {
                "id": next_image.id,
                "url": reverse("media_manager:media", args=(next_image,)),
                "mime-type": next_image.mime_type,
                "media_type": next_image.media_type,
            } if next_image else None
        })
