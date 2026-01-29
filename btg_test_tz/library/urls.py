from django.urls import path
from .views import BookListCreateView, BookEditDetailView, UserListCreateView, UserEditDetailView

urlpatterns = [
    path("books/", BookListCreateView.as_view()),
    path("books/book/<int:id>", BookEditDetailView.as_view()),
    path("users/", UserListCreateView.as_view()),
    path("users/user/<int:id>", UserEditDetailView.as_view()),
]