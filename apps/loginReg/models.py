from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from datetime import datetime
import re, bcrypt

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register_validation(self, postData):
        messages = []
        flag = False

        # no fields can be blank
        if not postData['name'] or not postData['username'] or not  postData['password'] or not postData['confirm_pw'] or not postData['date_hired']:
            flag = True
            messages.append('No fields can be blank')

        #name and username must be at least 3 characters
        if len(postData['name']) < 3 or len(postData['username']) < 3:
            flag = True
            messages.append('Name and username must be at least 3 characters long')

        # names can only be letters
        if not NAME_REGEX.match(postData['name']):
            flag = True
            messages.append('Name fields may only contain letters')

        # passwords must match
        if postData['password'] != postData['confirm_pw']:
            flag = True
            messages.append('Passwords do not match')

        # password must be at least 8 characters
        if postData['password'] < 8:
            flag = True
            messages.append('Password is too short')

        # date hired must be in the past
        if postData['date_hired']:
            date_obj = datetime.strptime(postData['date_hired'], '%Y-%m-%d')
            print '*'*20
            print date_obj, type(date_obj)
            print datetime.now(), type(datetime.now())

            if date_obj > datetime.now():
                    flag = True
                    messages.append('Date hired must be in the past')

        # username can't already be in database
        users = User.objects.filter(username__iexact=postData['username'])
        if users:
            flag = True
            messages.append('Your username is already in use')

        #if it worked, send the data back to views
        if not flag:
            pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

            user = User.objects.create(name= postData['name'],
            username=postData['username'],
            password = pw_hash, date_hired=postData['date_hired'])

            return(True, user)

        else:
            return(False, messages)

    def login_validation(self, postData):
        messages = []
        flag = False

        # must enter an email addres
        if len(postData['username']) < 1:
            flag = True
            messages.append('Please enter your username')

        # check if the user is in the datebase
        if len(postData['username']) > 0:
            user = User.objects.filter(username=postData['username'])

            if len(user) < 1:
                flag = True
                messages.append('User not found')
                print 'this is the user: ', user
        else:
            user = False

        # must enter a password
        if len(postData['password']) < 1:
            flag = True
            messages.append('Password too short')

        # if user is found in database, check that hashed passwords match
        if user:
            print "bcrypt result: "
            print (bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) == user[0].password)

            if not bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) == user[0].password:
                flag = True
                messages.append('Password is not valid')

        if flag:
            return (False, messages)
        else:
            return (True, user)

class User(models.Model):
      name = models.CharField(max_length=45)
      username = models.CharField(max_length=45)
      password = models.CharField(max_length=100)
      date_hired = models.DateField(null=True)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = UserManager()
