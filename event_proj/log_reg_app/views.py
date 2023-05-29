from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            password = request.POST.get('password')
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
                password = pw_hash
            )
            request.session['user_id'] = user.id
            return redirect("/events/dashboard")
    else: 
        return render(request, 'index.html')
    
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email = email)[0]
        request.session['user_id'] = user.id
        return redirect("/events/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")