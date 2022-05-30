import json
import random
from .login_required import LoginRequiredView
from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from ..models import MediaFile, Tag, TagAction


def get_next_image_set(tag: Tag):
    media_set = MediaFile.objects.exclude(tags=tag)
    offset = random.randint(0, tag.untagged_count()-21)
    return media_set[offset:offset+20]


class TagImagesView(LoginRequiredView):
    def get(self, request, tag):
        the_images = get_next_image_set(tag)
        if len(the_images) == 0:
            return redirect('media_manager:tag_list')
        ctx = {
            "the_images": the_images,
            "tag": tag
        }
        return render(request, 'media_manager/tag_images.html', context=ctx)

    def post(self, request, tag: Tag):
        post_data = json.loads(request.body)

        positive_images = MediaFile.objects.prefetch_related("tags").filter(id__in=post_data.get('positives'))
        negative_images = MediaFile.objects.prefetch_related("tags").filter(id__in=post_data.get('negatives'))
        tag_actions_to_delete = []
        tag_actions_to_create = []
        image: MediaFile
        for image in positive_images:
            if image.tags.contains(tag):
                # Image already tagged for this tag group.
                # Remove the tag so it can be replaced
                tag_actions_to_delete.append(image.tagaction_set.filter(tag=tag))
            tag_actions_to_create.append(TagAction(tag=tag, media_file=image, certainty=50, human_tagged=True, positive=True))
            # image.tags.add(tag,
            #                through_defaults={'certainty': 50, 'human_tagged': True, 'positive': True})

        for image in negative_images:
            if image.tags.contains(tag):
                # Image already tagged for this tag group.
                # Remove the tag so it can be replaced
                tag_actions_to_delete.append(image.tagaction_set.filter(tag=tag))
            tag_actions_to_create.append(TagAction(tag=tag, media_file=image, certainty=50, human_tagged=True, positive=False))
            # image.tags.add(tag,
            #                through_defaults={'certainty': 50, 'human_tagged': True, 'positive': False})

        if tag_actions_to_delete:
            deletion_queryset = tag_actions_to_delete.pop()
            for q in tag_actions_to_delete:
                deletion_queryset |= q
            deletion_queryset.delete()

        TagAction.objects.bulk_create(tag_actions_to_create)

        next_images = get_next_image_set(tag)
        return JsonResponse({
            "next_images": [{
                "id": next_image.id,
                "url": reverse("media_manager:media", args=(next_image,)),
                "mime-type": next_image.mime_type,
                "media_type": next_image.media_type,
            } for next_image in next_images]
        })
