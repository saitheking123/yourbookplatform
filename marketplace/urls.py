from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('signup/', views.signup, name='signup'),
    path('my-books/', views.my_books, name='my_books'), 
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),  # ✅
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),# ✅
    path('books/<int:book_id>/order/', views.request_to_buy, name='request_to_buy'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('seller-orders/', views.seller_orders, name='seller_orders'),
    path('accept-order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('about/', views.about, name='about'),
]
