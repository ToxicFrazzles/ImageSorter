from .login_required import LoginRequiredView
from django.views.static import serve
from django.http.response import HttpResponse
from ..models import Setting
from pathlib import Path

try:
    use_x_accel = Setting.objects.get(key='x_accel').value.lower() in ('true', 'yes', 'y', 'yeah', '1')
except Setting.DoesNotExist:
    use_x_accel = False

try:
    media_directory = Path(Setting.objects.get(key='media_home').value)
except Setting.DoesNotExist:
    pass


class MediaView(LoginRequiredView):
    def get(self, request, image):
        if use_x_accel:
            file_path = Path(image.file_path).relative_to(media_directory)
            response = HttpResponse()
            response["Content-Disposition"] = f"attachment; filename={file_path.name}"
            response["X-Accel-Redirect"] = f"/protected/{file_path}"
            return response

        return serve(request, image.file_path, document_root='/')
