import json

from .login_required import LoginRequiredView
from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django import forms
from ..models import TagGroup, Image, Tag


class ImageTagForm(forms.Form):
    image_field = forms.IntegerField(widget=forms.HiddenInput, label=None, error_messages=None)
    image: Image

    def __init__(self, tag_group: TagGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tag_options = []
        for tag in tag_group.tag_set.all():
            tag_options.append((tag.id, tag.name))
        tag_options.sort(key=lambda x: x[1])
        self.fields["tag"] = forms.ChoiceField(choices=tag_options)


class TagImageView(LoginRequiredView):
    def get(self, request, tag_group: TagGroup):
        the_image = Image.objects.exclude(tags__group=tag_group).order_by('?').first()
        ctx = {
            "tag_group": tag_group,
            "the_image": the_image,
            "tags": tag_group.tag_set.all().order_by('name'),
            "form": ImageTagForm(tag_group)
        }
        ctx['form'].fields['image_field'].initial = the_image.id
        return render(request, 'image_sorter/tag_image.html', context=ctx)

    def post(self, request, tag_group: TagGroup):
        post_data = json.loads(request.body)
        image = Image.objects.get(id=post_data.get("image_id"))
        if image.tags.filter(group=tag_group).count() > 0:
            # Image already tagged for this tag group.
            # Remove the tag so it can be replaced
            image.tags.remove(*tag_group.tag_set.all())
        tag = tag_group.tag_set.get(id=post_data.get("tag_id"))
        image.tags.add(tag)
        image.save()

        next_image = Image.objects.exclude(tags__group=tag_group).order_by('?').first()
        return JsonResponse({
            "next_image": {
                "id": next_image.id,
                "url": reverse("image_sorter:media", args=(next_image,))
            }
        })

        # form = ImageTagForm(tag_group, data=request.POST)
        #
        # if not form.is_valid():
        #     return redirect('image_sorter:tag_image', tag_group)
        # image_id = form.cleaned_data['image_field']
        # image = Image.objects.get(id=image_id)
        # tag_id = form.cleaned_data['tag']
        # tag = Tag.objects.get(id=tag_id, group=tag_group)
        # image.tags.add(tag)
        # image.save()
        # return redirect('image_sorter:tag_image', tag_group)
