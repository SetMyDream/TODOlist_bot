from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_destroy(self, instance):
        deleted_serializer = self.get_serializer(instance)
        super().perform_destroy(instance)
        return Response({"deleted_object": deleted_serializer.data})

# TODO: реалізувати функціонал очищення списків
class ClearAllTasksAPIView(APIView):
    def delete(self, request):
        Task.objects.all().delete()
        return Response({'message': 'Усі таски видалено'})


class TaskCompleteAPIView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.completed = True
            task.save()
            return Response({'message': f'Задачу {task_id} відмічено як виконану.'})
        except Task.DoesNotExist:
            return Response({'error': f'Задачу {task_id} не знайдено.'}, status=404)


class TaskCountAPIView(APIView):
    def get(self, request):
        # count = Task.objects.filter(deleted=False).count()
        count = Task.objects.count()
        return Response({'count': count})