from django.contrib import admin
from plandechicasapp.models import UserProfile
from plandechicasapp.models import FriendRequest
from plandechicasapp.models import Message
from plandechicasapp.models import DateType
from plandechicasapp.models import SpecialDate
from plandechicasapp.models import Notification
from plandechicasapp.models import NotificationType
from plandechicasapp.models import Product
from plandechicasapp.models import Pot
from plandechicasapp.models import Choice


admin.site.register(UserProfile)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(DateType)
admin.site.register(SpecialDate)
admin.site.register(Notification)
admin.site.register(NotificationType)
admin.site.register(Product)
admin.site.register(Pot)
admin.site.register(Choice)

def __unicode__(self):
    return self.title
