from django.utils import simplejson
from dajaxice.core import dajaxice_functions
from plandechicasapp.models import UserProfile, FriendRequest, Message, MessageThread, Notification, Product
from django.contrib.auth.models import User
from django.db.models import Q

def send_friend_request(request, request_message, receiver):
    user_to_search = User.objects.get(username=receiver)
    profile = user_to_search.get_profile()
    fRequest = FriendRequest()
    fRequest.sender = request.user.get_profile()
    fRequest.receiver = profile
    fRequest.text = request_message
    fRequest.sender_username = request.user.username
    fRequest.receiver_username = user_to_search.username
    fRequest.save()

dajaxice_functions.register(send_friend_request)

def send_message(request, message_text, receiver):
    user_to_search = User.objects.get(username=receiver)
    profile = user_to_search.get_profile()
    messageThread = MessageThread()
    message = Message()
    messageThread.sender = request.user.get_profile()
    messageThread.receiver = profile
    message.text = message_text
    message.save()
    messageThread.save()

dajaxice_functions.register(send_message)

def accept_friend_request(request, receiver):
    user_to_search = User.objects.get(username=receiver)
    receiver_profile = user_to_search.get_profile()
    sender_profile = request.user.get_profile()
    receiver_profile.friends.add(sender_profile)
    fRequest_to_search = FriendRequest.objects.get(Q(receiver_username=request.user.username)&Q(sender_username=receiver))
    fRequest_to_search.is_read = True
    fRequest_to_search.is_accepted = True
    fRequest_to_search.save()

dajaxice_functions.register(accept_friend_request)

def ignore_friend_request(request, receiver):
    fRequest_to_search = FriendRequest.objects.get(Q(receiver_username=request.user.username)&Q(sender_username=receiver))
    fRequest_to_search.is_read = True
    fRequest_to_search.save()

dajaxice_functions.register(ignore_friend_request)

def remove_notifications(request, name):
    notifications = Notification.objects.filter(Q(owner=request.user)&Q(notification_type__name__exact=name))
    notifications.delete()

dajaxice_functions.register(remove_notifications)

def add_fichaje(request, product):
    user_profile = request.user.get_profile()
    product_to_add = Product.objects.get(id=product)
    user_profile.fichajes.add(product_to_add)
    receiver_profile.friends.add(sender_profile)
    receiver_profile.save()

dajaxice_functions.register(add_fichaje)
