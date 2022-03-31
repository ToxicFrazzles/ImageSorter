from django import views
from django.shortcuts import render, redirect
from ..models import Image, TagGroup


class IndexView(views.View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'image_sorter/landing.html')
        ctx = {
            'image_count': Image.objects.count(),
            'tag_group_count': TagGroup.objects.count()
        }
        return render(request, 'image_sorter/dashboard.html', context=ctx)
