from django import views
from django.shortcuts import render, redirect
from ..models import MediaFile, TagGroup


class IndexView(views.View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'media_manager/landing.html')
        ctx = {
            'image_count': MediaFile.objects.count(),
            'tag_group_count': TagGroup.objects.count()
        }
        return render(request, 'media_manager/dashboard.html', context=ctx)
