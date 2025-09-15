from rest_framework import viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import MiniProject
from .serializers import MiniProjectSerializer
from .permissions import IsOwnerOrTrainer, IsTrainer

from django.contrib.auth.models import User
from .serializers import UserSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_trainees(request):
    trainee_group = Group.objects.filter(name='Trainee').first()
    if not trainee_group:
        return Response([])  # no trainees
    trainees = User.objects.filter(groups=trainee_group)
    serializer = UserSerializer(trainees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class MiniProjectViewSet(viewsets.ModelViewSet):
    serializer_class = MiniProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrTrainer]  # default
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'due_date', 'assigned_to']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Trainer').exists():
            # Trainers can see all projects
            return MiniProject.objects.all().order_by('-due_date')
        else:
            # Trainees see only assigned projects
            return MiniProject.objects.filter(assigned_to=user).order_by('-due_date')

    def get_permissions(self):
        # Trainers can create/edit/delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsTrainer]
        # Trainees can only view list/retrieve and update assigned project
        if self.action == 'partial_update':  # for status update by Trainee
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrTrainer]
        return super().get_permissions()