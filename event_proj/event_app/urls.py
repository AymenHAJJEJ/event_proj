from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard),
    path('create', views.create_event),
    path('<int:id>', views.event_detail),
    path('<int:id>/edit', views.update_event),
    path('<int:id>/delete', views.delete_event)
]