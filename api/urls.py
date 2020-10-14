from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, UserViewSet, UserView, MyAccView, GenreViewSet, \
    CategoryViewSet, TitleViewSet, CommentViewSet, ReviewViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('users/me/', MyAccView.as_view()),
    path(r'users/<str:username>/', UserView.as_view()),
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/email/', RegisterView.as_view()),
]
