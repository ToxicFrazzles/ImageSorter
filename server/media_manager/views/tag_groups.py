from .login_required import LoginRequiredView
from django.shortcuts import render
from ..models import TagGroup


class TagGroupsListView(LoginRequiredView):
    def get(self, request):
        ctx = {
            "tag_groups": TagGroup.objects.all()
        }
        return render(request, "media_manager/tag_groups_list.html", ctx)
