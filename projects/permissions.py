from rest_framework.permissions import BasePermission, SAFE_METHODS

def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

class IsTrainer(BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, 'Trainer')

class IsTrainee(BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, 'Trainee')

class IsOwnerOrTrainer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.assigned_to == request.user or is_in_group(request.user, 'Trainer')
