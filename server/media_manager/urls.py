from django.urls import path, register_converter
from . import views
from .models import MediaFile, Tag

app_name = 'media_manager'


class ImageURLConverter:
    regex = r"\d+"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value.id}"


class TagConverter:
    regex = r"\d+"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value.id}"


register_converter(ImageURLConverter, 'image')
register_converter(TagConverter, 'tag')

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('image/<image:image>/', views.MediaView.as_view(), name='media'),
    path('tags/list/', views.TagsListView.as_view(), name='tag_list'),
    path('tags/<tag:tag_id>/tag_image/', views.TagImageView.as_view(), name='tag_image'),
    path('tags/<tag:tag_id>/tag_images/', views.TagImagesView.as_view(), name='tag_images'),
    path('similar_images/', views.SimilarImagesView.as_view(), name='similar_images'),
    path('search/', views.SearchView.as_view(), name='search'),
]
