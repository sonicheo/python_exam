from django.db import models
import re
from datetime import date, datetime

class UsersManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First Name should be at least 2 characters'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last Name should be at least 2 characters'

        if len(post_data['birthday']) == 0:
            errors['birthday'] = 'Must put in a birthday date' 
        if post_data['birthday']:
            y = date.fromisoformat(post_data['birthday'])
            x = date.today()
            today = x.year
            user_birth_year = y.year
            print(user_birth_year)
            if (today - user_birth_year) < 13:
                errors['birthday_validation'] = 'Must be at least 13 years old'
        
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        

        for user in Users.objects.all():
            if user.email == post_data['email']:
                errors['email_unique'] = 'Email Already Taken'

        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords Do Not Match'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        return errors

    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        
        return errors

class JobsManager(models.Manager):
    def create_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 3:
            errors['title'] = 'Title must have at least 3 characters'
        if len(post_data['desc']) < 3:
            errors['desc'] = 'Description must have at least 3 characters'
        if len(post_data['location']) < 3:
            errors['location'] = 'Title must have at least 3 characters'
        return errors

    

class Users(models.Model):
    first_name = models.CharField(max_length = 15)
    last_name = models.CharField(max_length = 15)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    birthday = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()


class Jobs(models.Model):
    users = models.ManyToManyField(Users, related_name='job')
    title = models.CharField(max_length = 30)
    desc = models.CharField(max_length = 30)
    location = models.CharField(max_length = 30)
    category = models.CharField(max_length = 255, default = 'none')
    worked_on = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobsManager()
