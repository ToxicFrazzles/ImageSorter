from django.urls import path, register_converter
from . import views
from .models import Image, TagGroup

app_name = 'image_sorter'


class ImageURLConverter:
    regex = r"\d+"

    def to_python(self, value):
        return Image.objects.get(id=int(value))

    def to_url(self, value):
        return f"{value.id}"


class TagGroupConverter:
    regex = r"\d+"

    def to_python(self, value):
        return TagGroup.objects.get(id=int(value))

    def to_url(self, value):
        return f"{value.id}"


register_converter(ImageURLConverter, 'image')
register_converter(TagGroupConverter, 'tag_group')

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('image/<image:image>/', views.MediaView.as_view(), name='media'),
    path('tag_groups/list/', views.TagGroupsListView.as_view(), name="tag_groups_list"),
    path('tag_groups/<tag_group:tag_group>/tag_image/', views.TagImageView.as_view(), name='tag_image'),
]
