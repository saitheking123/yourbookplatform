from django.shortcuts import render, redirect
from .models import Book
from .models import *
from .forms import BookForm
from .forms import FeedbackForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def book_list(request):
    books = Book.objects.all().order_by('-created_at')

    query = request.GET.get('q')
    condition = request.GET.get('condition')

    if query:
        books = books.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(description__icontains=query)
        )

    if condition and condition != 'all':
        books = books.filter(condition=condition)

    return render(request, 'marketplace/book_list.html', {
        'books': books,
        'query': query,
        'condition': condition
    })


def add_book(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'marketplace/add_book.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'marketplace/signup.html', {'form': form})



@login_required
def my_books(request):
    books = Book.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'marketplace/my_books.html', {'books': books})

from django.http import HttpResponseForbidden

@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this book.")

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('my_books')
    else:
        form = BookForm(instance=book)

    return render(request, 'marketplace/edit_book.html', {'form': form})


@login_required
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this book.")
    
    if request.method == 'POST':
        book.delete()
        return redirect('my_books')
    
    return render(request, 'marketplace/delete_book.html', {'book': book})

from django.shortcuts import get_object_or_404, redirect
from .models import Book, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'marketplace/book_detail.html', {'book': book})

@login_required
def request_to_buy(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.seller == request.user:
        messages.error(request, "You cannot buy your own book.")
        return redirect('book_detail', book_id=book_id)

    if request.method == 'POST':
        delivery_type = request.POST.get('delivery_type')
        if not delivery_type:
            messages.error(request, "Please select a delivery method.")
            return redirect('book_detail', book_id=book_id)
            
        Order.objects.create(buyer=request.user, book=book, delivery_type=delivery_type)
        messages.success(request, "Your request has been sent to the seller.")
        return redirect('my_orders')
    return redirect('book_detail', book_id=book_id)

@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).select_related('book')
    return render(request, 'marketplace/my_orders.html', {'orders': orders})

@login_required
def seller_orders(request):
    # Show all orders for books owned by the seller
    books = Book.objects.filter(user=request.user)
    orders = Order.objects.filter(book__in=books).select_related('book', 'buyer').order_by('-created_at')
    return render(request, 'marketplace/seller_orders.html', {'orders': orders})


def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            return render(request, 'marketplace/feedback_thanks.html')
    else:
        form = FeedbackForm()
    return render(request, 'marketplace/feedback_form.html', {'form': form})

from django.views.decorators.http import require_POST

@login_required
@require_POST
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, book__user=request.user)
    if order.status == 'requested':
        order.status = 'accepted'
        order.save()
        messages.success(request, 'Order accepted successfully!')
    else:
        messages.error(request, 'Order cannot be accepted.')
    return redirect('seller_orders')


def about(request):
    return render(request, 'marketplace/about.html')
