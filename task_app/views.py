from django.shortcuts import render,redirect
from django.http import HttpResponse
from task_app.forms import *
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .serializers import *
from .models import *
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task

# <------Register page----->

def register(request):
    form = CustomUserForm()
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/my_login')
    return render(request,'register.html',{'form':form})

# <----Login page------>

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                auth.login(request,user)
                return redirect('/api')
    context = {'form':form}
    return render(request,'my_login.html',context=context)



# API Overview
@login_required(login_url='my_login')
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/task-list/',
        'Create' : '/task-create/',
        'Update' : '/task-update/<str:pk>/',
        'Delete' : '/task-delete/<str:pk>/',
    }
    return Response(api_urls)

# Read
@login_required(login_url='my_login')
@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many = True)
    return Response(serializer.data)




# CREATE
@login_required(login_url='my_login')
@api_view(['POST'])
def taskCreate(request):
    item = TaskSerializer(data=request.data)
 
    # validating for already existing data
    if Task.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

#UPDATE
@login_required(login_url='my_login')
@api_view(['POST'])
def taskUpdate(request, pk):
    item = Task.objects.get(pk=pk)
    data = TaskSerializer(instance=item, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

#DELETE
@login_required(login_url='my_login')
@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id = pk)
    task.delete()
    return Response("Task deleted successfully.")


# <--------logout----->

def user_logout(request):
    auth.logout(request)
    return redirect('/my_login')