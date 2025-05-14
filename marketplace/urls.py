from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('signup/', views.signup, name='signup'),
    path('my-books/', views.my_books, name='my_books'), 
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),  # ✅
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),  # ✅
]
