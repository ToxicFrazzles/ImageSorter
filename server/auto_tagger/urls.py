from django.urls import path, register_converter

from media_manager.models import MediaFile
from . import views

#
# class ImageURLConverter:
#     regex = r"\d+"
#
#     def to_python(self, value):
#         return MediaFile.objects.get(id=int(value))
#
#     def to_url(self, value):
#         return f"{value.id}"
#
#
# register_converter(ImageURLConverter, 'image')


urlpatterns = [
    path("auth/", views.AuthView.as_view(), name="challenge"),
    path('media/<image:media>/', views.MediaView.as_view(), name="media"),
]
