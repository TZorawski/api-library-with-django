from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_book', views.create),
    path('book_detail/<int:id>', views.get),
    path('list_book', views.get_all),
    path('edit_book/<int:id>', views.put),
    path('delete_book/<int:id>', views.delete),
]