from django.urls import path
from .views import *

urlpatterns = [
    path('', BoardView.as_view()),
    path('/<int:post_id>', BoardDetailView.as_view()),
]
