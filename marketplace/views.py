from django.shortcuts import render, redirect
from .models import Book
from .models import *
from .forms import BookForm
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
