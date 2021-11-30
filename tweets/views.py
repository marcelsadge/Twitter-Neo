from django.shortcuts import render, redirect

# Create your views here.

def splash(request):
    if request.user.is_authenticated:
        return redirect("/home")
    return render(request, "splash.html", {})

def login(request):
    return render(request, "login.html", {})

def register(request):
    return render(request, "register.html", {})

def homepage(request):
    return render(request, "homepage.html", {})