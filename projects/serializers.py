# projects/serializers.py
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import MiniProject

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

    def get_role(self, obj):
        if obj.groups.filter(name='Trainer').exists():
            return 'Trainer'
        elif obj.groups.filter(name='Trainee').exists():
            return 'Trainee'
        return None

class MiniProjectSerializer(serializers.ModelSerializer):
    # Use UserSerializer for nested representation
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    # Use PrimaryKeyRelatedField for writing (creating/updating)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True
    )

    class Meta:
        model = MiniProject
        fields = [
            'id', 'title', 'description', 'status', 'priority', 'due_date',
            'assigned_to', 'created_by', 'created_at', 'updated_at', 'assigned_to_id'
        ]
        read_only_fields = ['created_by']

    def create(self, validated_data):
        # Set created_by to the current user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def __init__(self, *args, **kwargs):
        super(MiniProjectSerializer, self).__init__(*args, **kwargs)
    
    # Safe way to filter assigned_to_id by Trainees
        trainee_group = Group.objects.filter(name='Trainee').first()
        if trainee_group:
         self.fields['assigned_to_id'].queryset = User.objects.filter(groups=trainee_group)
        else:
        # If Trainee group doesn't exist, fallback to empty queryset
         self.fields['assigned_to_id'].queryset = User.objects.none()
