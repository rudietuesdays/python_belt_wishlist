from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User

# Create your views here.
def index(request):
    print '*'*20
    print 'List of users objects:', User.objects.all()
    return render(request, 'loginReg_templates/index.html')

def register_user(request):
    postData = {
        'name': request.POST['name'],
        'username': request.POST['username'],
        'password': request.POST['password'],
        'confirm_pw': request.POST['confirm_pw'],
        'date_hired': request.POST['date_hired'],
    }

    #pull register method from models.py
    result = User.objects.register_validation(postData)

    #check true or false : user[0] is True, user[1] is false , which comes from the tuple in models.py
    if result[0]:
        print '*'*20
        print result[0], result[1]
        request.session['uid'] = result[1].id
        user_obj = result[1]

        context = {
            'user': user_obj
        }

        return redirect(reverse('wishList:dashboard'))

    #loop through messages showing errors if the registration wasn't successful
    else:
        for err in range(len(result[1])):
            messages.error(request, result[1][err])
        return redirect('/')

def login_user(request):

    postData = {
        'username': request.POST['login_user'],
        'password': request.POST['login_password'],
    }

    user = User.objects.login_validation(postData)

    print '*'*20
    print user[1]
    if user[0]:
        request.session['uid'] = user[1][0].id
        user_obj = user[1][0]
        context = {
            "user": user_obj
        }
        return redirect(reverse('wishList:dashboard'))

    else:
        for message in range(len(user[1])):
            messages.error(request, user[1][message])
        return redirect('/')

def logout_user(request):
    del request.session['uid']
    return redirect('/')
