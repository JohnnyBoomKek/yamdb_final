from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    roles_choices = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin")
    )
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=30, choices=roles_choices, default="user")
    confirmation_code = models.IntegerField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=250)
    year = models.PositiveSmallIntegerField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="titles", null=True)
    genre = models.ManyToManyField(Genre, related_name="titles", blank=True)
    description = models.TextField(blank=True)

    @property
    def rating(self):
        score = self.reviews.aggregate(rating=models.Avg('score'))
        return score['rating']

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)
