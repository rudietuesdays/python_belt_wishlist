from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User, Item, Wish

# Create your views here.

def index(request):
    user = User.objects.get(id=request.session['uid'])
    myItems = Item.objects.filter(user__id=request.session['uid'])
    otherItems = Item.objects.exclude(user__id=request.session['uid'])&Item.objects.exclude(wanted__user_id=request.session['uid'])
    wishes = Wish.objects.filter(user__id=request.session['uid'])


    context = {
        'user': user,
        'myItems': myItems,
        'otherItems': otherItems,
        'wishes': wishes,
    }

    return render(request, "wishList_templates/index.html", context)

def add_item(request):
    return render(request, 'wishList_templates/add_item.html')

def create_item(request):
    postData = {
        'item': request.POST['item'],
        'user_id': request.session.get('uid'),
    }

    result = Item.objects.validate(postData)

    if result[0]:
        return redirect(reverse('wishList:dashboard'))
    else:
        for err in range(len(result[1])):
            messages.error(request, result[1][err])
        return redirect(reverse('wishList:add'))

def view_item(request, id):
    item = Item.objects.get(id=id)
    user = User.objects.get(id = request.session['uid'])
    wish = Wish.objects.filter(item_id=item.id)

    # print item.item, wish[0].user.name

    context = {
        'item': item,
        'user': user,
        'wish': wish,
    }

    return render(request, "wishList_templates/item.html", context)

def delete_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect(reverse('wishList:dashboard'))

def join_item(request, id):
    user = User.objects.get(id=request.session['uid'])
    item = Item.objects.get(id=id)
    wish = Wish.objects.create(user_id=user.id, item_id=item.id)
    return redirect(reverse('wishList:dashboard'))

def remove_item(request, id):
    wish = Wish.objects.get(id=id)
    wish.delete()
    return redirect(reverse('wishList:dashboard'))
