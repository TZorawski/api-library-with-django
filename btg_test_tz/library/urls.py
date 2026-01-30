from django.urls import path
from .views import BookListCreateView, BookEditDetailView, UserListCreateView, UserEditDetailView, LoanListCreateView, LoanReturnView

urlpatterns = [
    path("books/", BookListCreateView.as_view()),
    path("books/book/<int:id>", BookEditDetailView.as_view()),
    path("users/", UserListCreateView.as_view()),
    path("users/user/<int:id>", UserEditDetailView.as_view()),
    path("loans/", LoanListCreateView.as_view()),
    path("loans/return/<int:loan_id>", LoanReturnView.as_view()),
]