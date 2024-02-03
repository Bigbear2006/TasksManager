from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, BasePermission
from . import models, serializers


class CanManageTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return obj.user == request.user or obj.project.main_user == request.user


class ProjectViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()


class TaskViewSet(ModelViewSet):
    permission_classes = (CanManageTask,)
    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()

