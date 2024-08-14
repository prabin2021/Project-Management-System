
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import User
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('/')

    return render(request, 'account/login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('rpassword', '')

        if name and email and password1 and password2:
            if password1 != password2:
                messages.error(request, "Passwords do not match!")
                print("Password not matched")
                return redirect('/signup/')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already taken!")
                print("Email already taken")
                return redirect('/signup/')

            try:
                user = User.objects.create_user(name=name, email=email, password=password1)
                print("User Created",user)
                messages.success(request, "Account created successfully!")
                return redirect('/login/')
            except IntegrityError:
                messages.error(request, "An error occurred during signup. Please try again.")
                print("Integrity error")
                return redirect('/signup/')
        else:
            messages.error(request, "All fields are required!")
            return redirect('/signup/')

    return render(request, 'account/signup.html')

@login_required
def logout(request,user):
    auth_logout(request)
    return redirect('base.html')
