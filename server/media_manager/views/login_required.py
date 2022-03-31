from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class LoginRequiredView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        return redirect("/")
