"""
URL configuration for todolistproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo_app.views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView, TaskCountAPIView, ClearAllTasksAPIView, TaskCompleteAPIView, TaskIncompleteAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-retrieve-update-destroy'),
    path('api/tasks/count/', TaskCountAPIView.as_view(), name='task-count'),
    path('api/tasks/clear-all/', ClearAllTasksAPIView.as_view(), name='clear_all_tasks'),
    path('api/tasks/<int:task_id>/complete/', TaskCompleteAPIView.as_view(), name='task-complete'),
    path('api/tasks/<int:task_id>/incomplete/', TaskIncompleteAPIView.as_view(), name='task-incomplete'),
]

