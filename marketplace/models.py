from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    condition = models.CharField(max_length=50, choices=[
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('used', 'Used'),
    ])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='book_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title
