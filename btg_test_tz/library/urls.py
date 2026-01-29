from django.urls import path
from .views import (BookListCreateView, BookEditDetailView)

urlpatterns = [
    path("books/", BookListCreateView.as_view()),
    path("books/book/<int:id>", BookEditDetailView.as_view()),
]