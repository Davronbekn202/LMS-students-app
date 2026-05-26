from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm,LoginForm
from firsapp.models import Student

def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            if user:
                Student.objects.create(user=user)
            try:
                login(request, user)
            except Exception as e:
                return redirect('login')
            return redirect('home')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'account/register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Username yoki parol noto‘g‘ri")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')

