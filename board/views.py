import json
import re
import bcrypt
import requests

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from .models import FreeBoard
from .validators import password_valid


class BoardView(View):
    """게시글 등록"""

    def post(self, request):
        try:
            data = json.loads(request.body)

            password = data["password"]
            title    = data["password"]
            content  = data["content"]

            """날씨API에서 현재 날씨 얻어오기"""
            weather = requests.get(
                'http://api.weatherapi.com/v1/current.json?key=41b7b28bf1ff4f59b4f10444220609&q=Seoul&aqi=no')\
                .json()['current']['condition']['text']

            password_check = password_valid(password)
            if not password_check[0]:
                return JsonResponse({'Message': password_check[1]}, status=400)

            hashed_password = bcrypt.hashpw(password.encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8')

            FreeBoard.objects.create(
                password = hashed_password,
                weather  = weather,
                title    = title,
                content  = content
            )
            return JsonResponse({'Message': 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)
