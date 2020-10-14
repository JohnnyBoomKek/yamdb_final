from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import random

from .models import CustomUser, Genre, Title, Category, Comment, Review
from .relations import SlugRelatedField


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def create(self, validated_data):
        email = validated_data['email']
        confirmation_code = f'{random.randrange(1, 10**6):06}'
        if (email and CustomUser.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        user = CustomUser.objects.create(
            email=email,
            is_active=True,
            role='User',
            confirmation_code=confirmation_code,
            password=make_password(confirmation_code),
            username=email.replace('@', '_').replace('.', '_'),
        )
        request = self.context.get("request")

        return self.data['email']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name',
                  'last_name', 'username', 'bio', 'role']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializerWrite(serializers.ModelSerializer):
    genre = SlugRelatedField(many=True, slug_field='slug',
                             queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')

        extra_kwargs = {'category': {'required': True},
                        'genre': {'required': False},
                        'year': {'required': False},
                        'description': {'required': False}
                        }


class TitleSerializerRead(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'genre',
                  'category', 'description', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    score = serializers.ChoiceField(choices=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment
