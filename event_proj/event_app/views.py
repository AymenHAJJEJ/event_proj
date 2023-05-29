from django.shortcuts import render, redirect
from log_reg_app.models import User
from django.contrib import messages
from .models import Event 


def dashboard(request):
    user_id = request.session.get('user_id')
    context = {
        'user' : User.objects.get(id=user_id),
        'events': Event.objects.all()
    }
    if 'user_id' not in request.session:
        return redirect("/")
    return render(request, 'dashboard.html', context)

def create_event(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        errors = Event.objects.event_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/events/dashboard")
        Event.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            scheduled=request.POST.get('scheduled'),
            location=request.POST.get('location'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude'),
            user=User.objects.get(id=user_id)
            )
        messages.success(request, 'Event successfully created')
        return redirect("/events/dashboard")
    else: 
        return render(request, 'dashboard.html')

def event_detail(request, id):
    event = Event.objects.get(id=id)
    user_id = request.session.get('user_id')
    if event:
        lat = event.latitude
        lon = event.longitude
        context = {
            'user' : User.objects.get(id=user_id),
            'event': event,
            'latitude': lat,
            'longitude': lon,
        }
        if 'user_id' not in request.session:
            return redirect("/")
        return render(request, 'detail.html', context)
    else:
        error_message = 'Map not found.'
        return render(request, 'error.html', {'error_message': error_message})

def update_event(request, id):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        errors = Event.objects.event_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/events/{id}/edit")
        else:
            event = Event.objects.get(id=id)
            event.title = request.POST.get('title')
            event.description = request.POST.get('description')
            event.location = request.POST.get('location')
            event.latitude = request.POST.get('latitude')
            event.longitude = request.POST.get('longitude')
            event.scheduled = request.POST.get('scheduled')
            event.user = User.objects.get(id=user_id)
            event.save()
            messages.success(request, 'Event successfully updated')
            return redirect("/events/dashboard")
    else:
        context={
            'user' : User.objects.get(id=user_id),
            'event': Event.objects.get(id=id)
        }
        if 'user_id' not in request.session:
            return redirect("/")
        return render(request, 'edit.html', context)

def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    return redirect("/events/dashboard")