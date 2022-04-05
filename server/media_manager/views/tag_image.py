import json
from .login_required import LoginRequiredView
from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.db.models import Count, Q
from django import forms
from ..models import TagGroup, MediaFile, Tag


def get_next_image(tag_group: TagGroup):
    media_set = MediaFile.objects.exclude(tags__group=tag_group)
    if tag_group.parent_tags.count() > 0:
        media_set = media_set.filter(tags__in=tag_group.parent_tags.all())
        media_set = media_set.annotate(num_parents=Count('tags')).filter(num_parents=tag_group.parent_tags.count())
    return media_set.filter(media_type=0).distinct().order_by('?').first()


class ImageTagForm(forms.Form):
    image_field = forms.IntegerField(widget=forms.HiddenInput, label=None, error_messages=None)
    image: MediaFile

    def __init__(self, tag_group: TagGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tag_options = []
        for tag in tag_group.tag_set.all():
            tag_options.append((tag.id, tag.name))
        tag_options.sort(key=lambda x: x[1])
        self.fields["tag"] = forms.ChoiceField(choices=tag_options)


class TagImageView(LoginRequiredView):
    def get(self, request, tag_group: TagGroup):
        the_image = get_next_image(tag_group)
        if the_image is None:
            return redirect('media_manager:tag_groups_list')
        ctx = {
            "tag_group": tag_group,
            "the_image": the_image,
            "tags": tag_group.tag_set.all().order_by('name'),
            "form": ImageTagForm(tag_group)
        }
        ctx['form'].fields['image_field'].initial = the_image.id
        return render(request, 'media_manager/tag_image.html', context=ctx)

    def post(self, request, tag_group: TagGroup):
        post_data = json.loads(request.body)
        image = MediaFile.objects.get(id=post_data.get("image_id"))
        if image.tags.filter(group=tag_group).count() > 0:
            # Image already tagged for this tag group.
            # Remove the tag so it can be replaced
            image.tags.remove(*tag_group.tag_set.all())
        tag = tag_group.tag_set.get(id=post_data.get("tag_id"))
        image.tags.add(tag)
        image.save()

        next_image = get_next_image(tag_group)
        return JsonResponse({
            "next_image": {
                "id": next_image.id,
                "url": reverse("media_manager:media", args=(next_image,)),
                "mime-type": next_image.mime_type,
                "media_type": next_image.media_type,
            }
        })

        # form = ImageTagForm(tag_group, data=request.POST)
        #
        # if not form.is_valid():
        #     return redirect('media_manager:tag_image', tag_group)
        # image_id = form.cleaned_data['image_field']
        # image = Image.objects.get(id=image_id)
        # tag_id = form.cleaned_data['tag']
        # tag = Tag.objects.get(id=tag_id, group=tag_group)
        # image.tags.add(tag)
        # image.save()
        # return redirect('media_manager:tag_image', tag_group)
