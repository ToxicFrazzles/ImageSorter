from .login_required import LoginRequiredView
from django.shortcuts import render
from ..models import Tag


class TagsListView(LoginRequiredView):
    def get(self, request):
        ctx = {
            "tags": Tag.objects.all()
        }
        return render(request, 'media_manager/tags_list.html', context=ctx)
