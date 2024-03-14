from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ThreadForm
from .models import Thread
from django.contrib.auth.decorators import login_required

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'forum/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('forummain')

            except IntegrityError:
               return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken'})

        else:
            return render(request, 'forum/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

@login_required
def logoutuser(request):
    # we only want to log someone out if the request is a POST
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
   if request.method == 'GET':
        return render(request, 'forum/login.html', {'form':AuthenticationForm()})
   else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password']) 
        if user is None:
            return render(request, 'forum/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('forummain')

def home(request):
        return render(request, 'forum/home.html')


def forummain(request):
      threads = Thread.objects.all().order_by('-created')
      return render(request, 'forum/forummain.html', {'threads':threads})

@login_required
def createthread(request):
    if request.method == 'GET':
        return render(request, 'forum/createthread.html', {'form':ThreadForm()})
    else:
         try:
            form = ThreadForm(request.POST)
            newthread = form.save(commit=False)
            #create a new todo object for me, and don't necessarily put it in the DB yet
            newthread.user = request.user
            #this way, we don't give people the option to create todos for other users
            newthread.save()
            return redirect('forummain')
         except ValueError:
             return render(request, 'forum/createthread.html', {'form':ThreadForm(), 'error':'Bad data passed in'})
             

def viewthread(request, thread_pk):
      thread = get_object_or_404(Thread, pk=thread_pk)
      return render(request, 'forum/viewthread.html', {'thread':thread})

@login_required
def editthread(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk, user=request.user)
    if request.method == 'GET':
        thread = get_object_or_404(Thread, pk=thread_pk)
        form = ThreadForm(instance=thread)
        return render(request, 'forum/editthread.html', {'form':form})
    else:
        form = ThreadForm(request.POST, instance=thread)
        
        editedthread = form.save(commit=False)
        editedthread.save()
        return redirect('forummain')

@login_required
def deletethread(request, thread_pk):
     thread = get_object_or_404(Thread, pk=thread_pk, user=request.user)
     if request.method == 'POST':
          
          thread.delete()
          return redirect('forummain')



      
