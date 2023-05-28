from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First Name should be at least 2 characters'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last Name should be at least 2 characters'
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid email address!'
        emailCheck = self.filter(email = post_data['email'])
        if emailCheck:
            errors['email'] = 'Email already exists!'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords must match'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
