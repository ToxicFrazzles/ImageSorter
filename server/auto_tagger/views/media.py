from django.http import HttpRequest, HttpResponse, Http404
from django.views import View
from media_manager.models import MediaFile
from django.views.static import serve
from django.conf import settings
from pathlib import Path


class MediaView(View):
    def get(self, request: HttpRequest, media: int):
        if request.session.get("auto_tagger", None) is None:
            raise Http404
        media = MediaFile.objects.get(id=media)
        if settings.USE_XACCEL_FOR_MEDIA:
            file_path = Path(media.file_path).relative_to(settings.MEDIA_HOME_DIRECTORY)
            response = HttpResponse()
            response["Content-Type"] = media.mime_type
            response["Content-Disposition"] = f"inline; filename={file_path.name}"
            response["X-Accel-Redirect"] = f"/protected/{file_path}"
            return response

        return serve(request, media.file_path, document_root='/')
