from django.shortcuts import render

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


class TaskCountAPIView(APIView):
    def get(self, request):
        # count = Task.objects.filter(deleted=False).count()
        count = Task.objects.count()
        return Response({'count': count})