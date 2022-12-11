import json

from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from ..models import Tagger


@method_decorator(csrf_exempt, name="dispatch")
class AuthView(View):
    def get(self, request: HttpRequest):
        challenge = Tagger.get_challenge()
        request.session["auto_tagger_challenge"] = challenge
        return JsonResponse({
            "challenge": challenge
        })

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        if (
                "client_id" not in data
                or "response" not in data
                or "auto_tagger_challenge" not in request.session
        ):
            request.session.delete("auto_tagger_challenge")
            return JsonResponse({
                "Error": "Authentication failed",
                "Reason": "Missing required data",
            })
        try:
            tagger = Tagger.objects.get(client_id=data["client_id"])
        except Tagger.DoesNotExist:
            request.session.delete("auto_tagger_challenge")
            return JsonResponse({
                "Error": "Authentication failed"
            })
        if not tagger.can_auth(request.session["auto_tagger_challenge"], data["response"]):
            request.session.delete("auto_tagger_challenge")
            return JsonResponse({
                "Error": "Authentication failed"
            })
        request.session.delete("auto_tagger_challenge")
        request.session["auto_tagger"] = tagger.id
        return JsonResponse({
            "Success": "Authentication successful"
        })
