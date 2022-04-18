import json
from .login_required import LoginRequiredView
from ..models import MediaFile
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from pathlib import Path


class SimilarImagesView(LoginRequiredView):
    def get(self, request):
        the_image = MediaFile.objects.filter(media_type=0).exclude(similar_to=None).order_by('?').first()
        if the_image is None:
            return redirect('media_manager:index')
        ctx = {
            'image': the_image,
            'similars': the_image.similar_to.all()
        }
        return render(request, 'media_manager/similar_images.html', context=ctx)

    def post(self, request: HttpRequest):
        json_data = json.loads(request.body)
        the_image = MediaFile.objects.get(id=json_data.get('image'))
        similar_to = MediaFile.objects.get(id=json_data.get('similar_to'))

        if the_image.x_resolution > similar_to.x_resolution or the_image.y_resolution > similar_to.y_resolution:
            old_file = similar_to.file_path
            similar_to.file_path = the_image.file_path
            Path(old_file).unlink()
        the_image.delete()
        similar_to.save()

        return JsonResponse({"success": True})
