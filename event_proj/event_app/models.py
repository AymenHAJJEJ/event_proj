from django.db import models
from log_reg_app.models import User


class EventManager(models.Manager):
    def event_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 3:
            errors['title'] = 'Title should be at least 3 characters'
        if len(post_data['description']) < 3:
            errors['description'] = 'Description should be at least 3 characters'
        if len(post_data['location']) < 3:
            errors['location'] = 'Location should be at least 3 characters'
        if (post_data['scheduled']) == "":
            errors['scheduled'] = 'Please enter a date and time'
        if (post_data['latitude']) == "":
            errors['latitude'] = 'Please enter a Latitude'
        if (post_data['longitude']) == "":
            errors['longitude'] = 'Please enter a Longitude'
        return errors


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    user = models.ForeignKey(User, related_name="events", on_delete = models.CASCADE)
    scheduled = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventManager()