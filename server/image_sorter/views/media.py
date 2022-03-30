from .login_required import LoginRequiredView
from django.views.static import serve


class MediaView(LoginRequiredView):
    def get(self, request, image):
        return serve(request, image.file_path, document_root='/')
