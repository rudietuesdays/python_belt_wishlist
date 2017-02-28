from __future__ import unicode_literals
from django.db import models
from ..loginReg.models import User

# Create your models here.
class ItemManager(models.Manager):
    def validate(self, postData):
        messages = []
        flag = False

        if not postData['item']:
            flag = True
            messages.append('Item field cannot be blank')

        elif len(postData['item']) < 3:
            flag = True
            messages.append('Item name must be at least three characters')

        if not flag:
            item =  Item.objects.create(item=postData['item'], user_id=postData['user_id'])
            return (True, item)
        else:
            return (False, messages)


class Item(models.Model):
    item = models.CharField(max_length=45)
    user = models.ForeignKey(User, related_name='wisher')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ItemManager()

class Wish(models.Model):
    item = models.ForeignKey(Item, related_name='wanted')
    user = models.ForeignKey(User, related_name='wanter')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
