from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group


from django.contrib import messages, auth

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'You are now registered and can log in')
            login(request, user)
            
            return redirect('index')

        else:
            messages.error(request, 'An error occured during registration')
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)

# Create your views here.
def loginUser(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not Exist!')
            return redirect('loginUser')  

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            next_url = request.session.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid Password!')

            return redirect('loginUser')    
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.success(request, 'You are now log out')
    return redirect('loginUser')

    
@login_required(login_url='loginUser')
def admin_logout(request):
    logout(request)
    messages.success(request, 'You are now log out')
    return redirect('loginUser')
    




