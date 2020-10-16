from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .filters import TitleFilter
from .models import CustomUser, Comment, Genre, Review, Title, Category
from .permissions import (IsAdminPermission, IsSuperuserPermission,
                          IsAuthorOrAdminorReadOnlyPermission)
from .serializers import (UserRegistrationSerializer, UserSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializerWrite, TitleSerializerRead)


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAdminPermission, ]
    # Переопределяя get_queryset тесты отказываются работать, хотя в postman'e все вроде как нормально

    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, username):
        user = CustomUser.objects.get(username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = CustomUser.objects.get(username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyAccView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # Переопределяя get_queryset тесты отказываются работать, хотя в postman'e все вроде как нормально

    def get(self, request):
        user = CustomUser.objects.get(username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = CustomUser.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    permission_classes = [IsSuperuserPermission]

    def get_object(self):

        if self.request.method != 'DELETE':
            raise MethodNotAllowed(self.request.method)
        return get_object_or_404(Genre, slug=self.kwargs['pk'])


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperuserPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def get_object(self):

        if self.request.method != 'DELETE':
            raise MethodNotAllowed(self.request.method)
        return get_object_or_404(Category, slug=self.kwargs['pk'])


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    serializer_class = TitleSerializerRead
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsSuperuserPermission]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleSerializerRead
        else:
            return TitleSerializerWrite

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer_class()

        serializer = serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes_by_action = {
        'update': [IsAuthorOrAdminorReadOnlyPermission],
        'partial_update': [IsAuthorOrAdminorReadOnlyPermission],
        'destroy': [IsAuthorOrAdminorReadOnlyPermission, ],
    }

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        if self.get_queryset().filter(author=self.request.user):
            raise ValidationError(
                detail={'message': 'Вы уже оставляли отзыв на данное произведение!'})
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes_by_action = {
        'update': [IsAuthorOrAdminorReadOnlyPermission],
        'partial_update': [IsAuthorOrAdminorReadOnlyPermission],
        'destroy': (IsAuthorOrAdminorReadOnlyPermission,),
    }

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
