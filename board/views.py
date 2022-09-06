import json
import bcrypt
import requests

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from .models import FreeBoard
from .validators import password_valid


class BoardView(View):
    
    """게시글 등록 API"""
    def post(self, request):
        try:
            data = json.loads(request.body)

            password = data["password"]
            title    = data["title"]
            content  = data["content"]

            """날씨API에서 현재 날씨 얻어오기"""
            weather = requests.get(
                'http://api.weatherapi.com/v1/current.json?key=41b7b28bf1ff4f59b4f10444220609&q=Seoul&aqi=no')\
                .json()['current']['condition']['text']

            """비밀번호 유효성 검사"""
            password_check = password_valid(password)
            if not password_check[0]:
                return JsonResponse({'Message': password_check[1]}, status=400)

            """비밀번호 암호화"""
            hashed_password = bcrypt.hashpw(password.encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            """자유게시판 글 생성"""
            FreeBoard.objects.create(
                password = hashed_password,
                weather  = weather,
                title    = title,
                content  = content
            )
            return JsonResponse({'Message': 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)

    "게시글 리스트 API"
    def get(self, request):
        """ 페이지 1부터 1++ """
        page = request.GET.get('page', None) 
        page_count = int(request.GET.get('page_count', 20)) # QueryString으로 page_count보내지않은경우 default 20
        # 한페이지 내에서 모든 게시글
        if not page:
            postings = FreeBoard.objects.all().order_by('-created_at')
        # 웹 스크롤링시 pagenation 기능 default page_count = 20 
        else:
            page = int(page)
            postings = FreeBoard.objects.all().order_by('-created_at')[(page-1)*page_count:page*page_count]

        results = [
            {
                'id'        : post.id,
                'title'     : post.title,
                'content'   : post.content,
                'weather'   : post.weather,
                'created_at': post.created_at,
                'updated_at': post.updated_at
            }
            for post in postings
        ]

        return JsonResponse({'results': results}, status=200)


class BoardDetailView(View):

    def get(self, request, post_id):
        try:
            post = FreeBoard.objects.get(id = post_id)
            notice_detail = {
                'id'        : post.id,
                'title'     : post.title,
                'content'   : post.content,
                'weather'   : post.weather,
                'created_at': post.created_at,
                'updated_at': post.updated_at
            }

            return JsonResponse(notice_detail, status = 201)
        except FreeBoard.DoesNotExist:
            return JsonResponse({'Message': 'DOES_NOT_EXIST'}, status = 404)


    def put(self, request, post_id):
        try:
            data = json.loads(request.body)
            post = FreeBoard.objects.get(id = post_id)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), post.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=401)


            post = FreeBoard.objects.filter(id = post_id)
            title = data['title']
            content = data['content']

            post.update(title=title, content=content)

            return JsonResponse({'Message': 'EDIT_SUCCESS'}, status = 200)
        except FreeBoard.DoesNotExist:
            return JsonResponse({'Message': 'DOES_NOT_EXIST'}, status = 404)

    """ delete는 body로 password전달 불가능 >> header에 담기 """
    def delete(self, request, post_id):
        try:
            password = request.META['HTTP_PASSWORD']
            post = FreeBoard.objects.get(id = post_id)

            if not bcrypt.checkpw(password.encode('utf-8'), post.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=401)

            post.delete()

            return JsonResponse({'Message': 'DELETE_SUCCESS'}, status = 200)
        except FreeBoard.DoesNotExist:
            return JsonResponse({'Message': 'DOES_NOT_EXIST'}, status = 404)


