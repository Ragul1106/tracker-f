from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MiniProjectViewSet, UserDetailView
from .views import current_user, list_trainees

router = DefaultRouter()
router.register(r'projects', MiniProjectViewSet, basename='miniproject')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/me/', current_user, name='current-user'),
    path('users/trainees/', list_trainees, name='list-trainees'),
]