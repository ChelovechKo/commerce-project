from symtable import Class

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    FRACTION_CHOICES = [
        ("", "— No fraction —"),
        ("College of Winterhold", "College of Winterhold"),
        ("Dark Brotherhood", "Dark Brotherhood"),
        ("Thieves Guild", "Thieves Guild"),
        ("Companions", "Companions"),
        ("Imperial Legion", "Imperial Legion"),
        ("Stormcloaks", "Stormcloaks"),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=False, unique=True)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    fraction = models.CharField(max_length=100, choices=FRACTION_CHOICES, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0, blank=False)
    img = models.ImageField(upload_to='listings/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_listings')
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    user_win = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_win_listings', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlisted_by")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"User {self.user.username} watching {self.listing.name}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    create_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()