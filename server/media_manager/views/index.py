from django import views
from django.shortcuts import render, redirect
from ..models import MediaFile, MediaType, Tag


class IndexView(views.View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'media_manager/landing.html')
        ctx = {
            'image_count': MediaFile.objects.filter(media_type=MediaType.IMAGE).count(),
            'video_count': MediaFile.objects.filter(media_type=MediaType.VIDEO).count(),
            'unknown_count': MediaFile.objects.filter(media_type=MediaType.UNKNOWN).count(),
            'tag_count': Tag.objects.count(),
            'similar_images': MediaFile.objects.exclude(similar_to=None).count()
        }
        return render(request, 'media_manager/dashboard.html', context=ctx)
