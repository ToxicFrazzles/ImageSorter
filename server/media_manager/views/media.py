from ..models import MediaFile
from .login_required import LoginRequiredView
from django.views.static import serve
from django.http.response import HttpResponse
from django.conf import settings
from pathlib import Path


class MediaView(LoginRequiredView):
    def get(self, request, image: MediaFile):
        if settings.USE_XACCEL_FOR_MEDIA:
            file_path = Path(image.file_path).relative_to(settings.MEDIA_HOME_DIRECTORY)
            response = HttpResponse()
            response["Content-Type"] = image.mime_type
            response["Content-Disposition"] = f"inline; filename={file_path.name}"
            response["X-Accel-Redirect"] = f"/protected/{file_path}"
            return response

        return serve(request, image.file_path, document_root='/')
