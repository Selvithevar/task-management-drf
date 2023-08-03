from django.urls import path,include
from django.http import HttpResponse
from . import views as ev

urlpatterns = [
    # path('',ev.home,name='home'),
    path('',ev.register,name='register'),
    path('my_login',ev.my_login,name='my_login'),
    path('user_logout/',ev.user_logout,name='user_logout'), 

    # - CRUD operations
    # - CREATE TASK
    path('api/', ev.apiOverview, name="api-overview"),
    path('task-list/', ev.taskList, name="task-list"),
    path('task-create/', ev.taskCreate, name="task-Create"),
    path('task-update/<str:pk>/', ev.taskUpdate, name="task-update"),
    path('task-delete/<str:pk>/', ev.taskDelete, name="task-delete"),
]