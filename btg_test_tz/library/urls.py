from django.urls import path
from .views import (
    BookListCreateView, 
    BookEditDetailView,
    UserListCreateView,
    UserEditDetailView,
    LoanListCreateView,
    LoanReturnView,
    UserLoansListView,
    BookAvailabilityView,
    LoanListByUserView,
    LoanActivetedList
)


urlpatterns = [
    path("books/", BookListCreateView.as_view()),
    path("books/book/<int:id>", BookEditDetailView.as_view()),
    path("books/book/<int:id>/availability", BookAvailabilityView.as_view()),
    path("users/", UserListCreateView.as_view()),
    path("users/user/<int:id>", UserEditDetailView.as_view()),
    path("users/user/<int:id>/loans", UserLoansListView.as_view()),
    path("loans/", LoanListCreateView.as_view()),
    path("loans/activated", LoanActivetedList.as_view()),
    path("loans/return/<int:id>", LoanReturnView.as_view()),
    path("loans/user/<int:id>", LoanListByUserView.as_view()),
]