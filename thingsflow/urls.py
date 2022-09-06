from django.urls import path, include

urlpatterns = [
    path('api/board', include('board.urls')),
]
