from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from . models import Room, Topic
from .forms import  Roomform
#creat a dictionary list of rooms

#Creat a fucntion base view for home 
def loginview(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('Home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exit')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Username OR password does not exit')
    context = {'page': page}
    return render(request, 'base/login_registration.html', context)
 
def logoutUser(request):
   logout(request)
   return redirect('Home')
   
   
def registerUser(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'An erro occured during registration')
    
            
    return render(request, 'base/login_registration.html', {'form': form})

def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q,) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count
    contxt = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', contxt)

def homepage(request):
    return render(request, 'indexfirst.html')

#Creat a fucntion base view for room
def room(request, pk):
    rooms = Room.objects.get(id=pk) 
    context = {'room': rooms}
    return render(request, 'base/room.html', context)

@login_required(login_url='loginpage')
def  createRoom(request):
    form = Roomform()
    if request.method == 'POST':
        form = Roomform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
        
    context = {'form': form}
    return render(request, "base/room_from.html", context)

@login_required(login_url='loginpage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)
    
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    
    if request.method == 'POST':
        form = Roomform(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
    
    contxt = {'form': form}
    return render(request, 'base/room_from.html', contxt)

@login_required(login_url='loginpage')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    return render(request, "base/delete.html", {'obj': room})