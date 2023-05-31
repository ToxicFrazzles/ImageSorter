from django.http import HttpRequest
from django.views import View
from django.shortcuts import render
from .login_required import LoginRequiredView


class SearchView(LoginRequiredView):
    def get(self, request: HttpRequest):
        ctx = {}
        return render(request, "media_manager/search.html", context=ctx)
