from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

from plandechicasapp.models import UserProfile
from plandechicasapp.models import SpecialDate, Pot, Choice, Product
from plandechicasapp.models import Notification
from plandechicasapp.forms import LoginForm, EditProfileForm, WhatForForm, WhoForm
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import login_required
from plandechicasapp.models import Message, FriendRequest
from django.db.models import Q
from itertools import chain


from datetime import date
from datetime import datetime
from calendar import monthrange
from calendar import HTMLCalendar


#NOTIFICATIONS
def notifications_count(request, name):
    notifications = Notification.objects.filter(Q(owner=request.user)&Q(notification_type__name__exact=name))
    num_notifications = notifications.count()
    return num_notifications


#USERS
# Login form to authenticate user
def login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            # if form is valid
            if request.POST.has_key('remember_me'):
                request.session.set_expiry(1209600)
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if (user is not None) and (user.is_active):
                auth.login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/login/")
        else:
            form = LoginForm()
            return render_to_response('users/login.html', 
                                {'form': form}, 
                                context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

# Sign up
def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/dashboard/")
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            # if username exists TODO
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            firstname = request.POST.get('firstname', '')
            lastname = request.POST.get('lastname', '')
            # Modify musician
            user = User.objects.create_user(username=username, email=email, password=password)
            user.get_profile().first_name = firstname
            user.get_profile().last_name = lastname
            user.get_profile().save()
            user = auth.authenticate(username=username, password=password)
            if (user is not None) and (user.is_active):
                auth.login(request, user)
                return HttpResponseRedirect("/dashboard/")
            else:
                return HttpResponseRedirect("/login/")
        else:
            return render_to_response('users/signup.html', 
                                {}, 
                                context_instance=RequestContext(request))

#logout
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def xd_receiver(request):
    return render_to_response('xd_receiver.html')


#FRONTEND
def home(request):
    if request.user.is_authenticated():
        # If user is logged in, redirect to dashboard
        form = LoginForm()
        return render_to_response('frontend/home.html', 
                                {'form': form}, 
                                context_instance=RequestContext(request))
    else:
        # If user is not logged in, redirect to home page
        form = LoginForm()
        return render_to_response('frontend/home.html', 
                                {'form': form}, 
                                context_instance=RequestContext(request))

def about(request):
    return "hoa"

def view_profile(request, paramuser):
    username = request.user.username
    user_to_search = User.objects.get(username=paramuser)
    my_profile = False
    if username == paramuser:
        my_profile = True
    profile = user_to_search.get_profile()
    special_dates = SpecialDate.objects.filter(owner=user_to_search)

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'message':
            message_text = request.POST.get('action', '')
            message = Message()
            message.sender = request.user.get_profile()
            message.receiver = profile
            message.text = request.POST.get('request_message', '')
            message.save()
            return HttpResponseRedirect(request.path)
        else:
            fRequest = FriendRequest()
            fRequest.sender = request.user.get_profile()
            fRequest.receiver = profile
            fRequest.text = request.POST.get('message_text', '')
            fRequest.save()
            return HttpResponseRedirect(request.path)
    else:
        return render_to_response('website/user_profile.html',
            {'username': username, 
            'special_dates': special_dates,
            'my_profile': my_profile,
            'profile': profile,
            'calendar_num_notifications': calendar_num_notifications,
            'calendar_num_notif_zero':calendar_num_notif_zero,
            'friend_num_notifications': friend_num_notifications,
            'friend_num_notif_zero':friend_num_notif_zero,
            'pot_num_notifications': pot_num_notifications,
            'pot_num_notif_zero' : pot_num_notif_zero},
            context_instance=RequestContext(request))

#DASHBOARD
@login_required
def dashboard(request):
    username = request.user.username

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    return render_to_response('website/web_base.html',
        {'username': username,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero},
        context_instance=RequestContext(request))


@login_required
def view_self_profile(request):
    username = request.user.username
    profile = request.user.get_profile()
    special_dates = SpecialDate.objects.filter(owner=profile)

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    my_profile = True

    return render_to_response('website/user_profile.html',
        {'username': username,
        'special_dates': special_dates,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero,
        'my_profile' : my_profile,
        'profile': profile},
        context_instance=RequestContext(request))

@login_required
def edit_profile(request):
    username = request.user.username
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect('/')
        else:
            print profile_form.errors 
            return HttpResponseRedirect('/')
    else:
        profile_form = EditProfileForm(instance=request.user.get_profile())
        return render_to_response('dashboard/edit_profile.html', 
                                {'username': username,'profile_form': profile_form}, 
                                context_instance=RequestContext(request))

@login_required
def view_messages(request):
    username = request.user.username
    user = request.user.get_profile()
    #messages = Message.objects.filter(sender=user)
    messages = Message.objects.order_by('date')
    #messages.query.group_by = ['receiver']
    return render_to_response('dashboard/messages.html',
        {'username': username, 'messages':messages},
        context_instance=RequestContext(request))

@login_required
def view_friends(request):
    username = request.user.username
    user_friends = request.user.get_profile().friends

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    return render_to_response('website/friends.html',
        {'username': username,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero,
        'friends':user_friends},
        context_instance=RequestContext(request))

@login_required
def view_friend_requests(request):
    username = request.user.username
    user = request.user.get_profile()
    friendrequests = FriendRequest.objects.filter(Q(receiver_username=username)&Q(is_accepted=False)&Q(is_read=False))
    acceptedfrequests = FriendRequest.objects.filter(Q(receiver_username=username)&Q(is_accepted=True))
    readfrequests = FriendRequest.objects.filter(Q(receiver_username=username)&Q(is_read=True)&Q(is_accepted=False))
    #friendrequests = FriendRequest.objects.order_by('date')

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    return render_to_response('website/friend_requests.html',
        {'username': username, 
        'friendrequests':friendrequests, 
        'acceptedfrequests':acceptedfrequests, 
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero,
        'readfrequests':readfrequests}, 
        context_instance=RequestContext(request))

@login_required
def view_friend_addition(request):
    username = request.user.username
    user_friends = request.user.get_profile().friends

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    return render_to_response('website/add_friend.html',
        {'username': username,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero,
        'friends':user_friends},
        context_instance=RequestContext(request))

@login_required
def view_pinkmoments_generator(request):
    username = request.user.username


    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    return render_to_response('website/pinkmoments_generator.html',
        {'username': username, 
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero},
        context_instance=RequestContext(request))

@login_required
def view_calendar(request):
    username = request.user.username
    today = date.today()
    year = today.year
    month = today.month
    notifications = Notification.objects.filter(Q(owner=request.user)&Q(notification_type__name__exact='calendar'))
    num_notifications = notifications.count()
    special_dates = SpecialDate.objects.filter(owner=request.user)
    pots = Pot.objects.filter(Q(owner=request.user)&Q(date__year=year, date__month=month))
    obj_list = special_dates.filter(date__year=year, date__month=month)
    obj_list = list(chain(obj_list, pots))
    if not obj_list:
        obj_list = ""

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    return render_to_response('dashboard/calendar.html',
        {'username': username, 
        'special_dates': special_dates, 
        'obj_list': obj_list,
        'notifications': notifications,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero,
        'year': year, 
        'month': month},
        context_instance=RequestContext(request))

@login_required
def view_other_calendar(request, month):
    username = request.user.username
    today = date.today()
    year = today.year
    month = int(month)

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False


    special_dates = SpecialDate.objects.filter(owner=request.user)
    pots = Pot.objects.filter(Q(owner=request.user)&Q(date__year=year, date__month=month))
    obj_list = special_dates.filter(date__year=year, date__month=month)
    obj_list = list(chain(obj_list, pots))
    if not obj_list:
        obj_list = ""
    return render_to_response('dashboard/calendar.html',
        {'username': username, 
        'special_dates': special_dates, 
        'obj_list': obj_list, 
        #'notifications': notifications,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero,
        'year': year, 
        'month': month},
        context_instance=RequestContext(request))


@login_required
def view_pots(request):
    username = request.user.username

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False


    pots = Pot.objects.filter(owner=request.user)
    if not pots:
        pots = ""

    return render_to_response('website/pots_list.html',
        {'username': username,
        'pots': pots,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero,
        },
        context_instance=RequestContext(request))

@login_required
def view_pot_details(request, pot_id):
    username = request.user.username

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    pot = Pot.objects.get(Q(owner=request.user)&Q(id=pot_id))

    pot_user_list = pot.user_list
    pot_user_number = pot_user_list.count()
    if(pot_user_number==0):
        pot_user_number=1
    how_much_pay = (pot.price / pot_user_number ) 

    return render_to_response('website/pot_details.html',
        {'username': username,
        'pot': pot,
        'how_much_pay': how_much_pay,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero,
        },
        context_instance=RequestContext(request))

@login_required
def view_what_for(request, pot_id):
    username = request.user.username

     #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    if (pot_id!='0'):
        pot = Pot.objects.get(Q(owner=request.user)&Q(id=pot_id))
        if request.method == 'POST':
            if not pot:    
                what_for_form = WhatForForm(request.POST)
            else:
                what_for_form = WhatForForm(request.POST, instance=pot)
            if what_for_form.is_valid():
                what_for = what_for_form.save(commit=False)
                what_for.owner = request.user.get_profile()
                what_for.save()
                what_for.user_list.add(request.user.get_profile())
                return HttpResponseRedirect('/pots/'+str(what_for.id)+'/what_for/')
            else:
                print what_for_form.errors 
                return HttpResponseRedirect('/pots')
        else:
            what_for_form = WhatForForm(instance=pot)
            return render_to_response('website/pot_what_for.html', 
                                    {'username': username,
                                    'what_for_form': what_for_form,
                                    'calendar_num_notifications': calendar_num_notifications,
                                    'calendar_num_notif_zero':calendar_num_notif_zero,
                                    'friend_num_notifications': friend_num_notifications,
                                    'friend_num_notif_zero':friend_num_notif_zero,
                                    'pot_num_notifications': pot_num_notifications,
                                    'pot_num_notif_zero' : pot_num_notif_zero,
                                    'pot': pot}, 
                                    context_instance=RequestContext(request))
    else:
        if request.method == 'POST':
            what_for_form = WhatForForm(request.POST)
            if what_for_form.is_valid():
                what_for = what_for_form.save(commit=False)
                what_for.owner = request.user.get_profile()
                what_for.save()
                what_for.user_list.add(request.user.get_profile())
                return HttpResponseRedirect('/pots/'+str(what_for.id)+'/what_for/')
            else:
                print what_for_form.errors 
                return HttpResponseRedirect('/pots')
        else:
            what_for_form = WhatForForm(request.POST)
            return render_to_response('website/pot_what_for.html', 
                                    {'username': username,
                                    'calendar_num_notifications': calendar_num_notifications,
                                    'calendar_num_notif_zero':calendar_num_notif_zero,
                                    'friend_num_notifications': friend_num_notifications,
                                    'friend_num_notif_zero':friend_num_notif_zero,
                                    'pot_num_notifications': pot_num_notifications,
                                    'pot_num_notif_zero' : pot_num_notif_zero,
                                    'what_for_form': what_for_form}, 
                                    context_instance=RequestContext(request))

@login_required
def view_who(request, pot_id):
    username = request.user.username

     #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    pot = Pot.objects.get(Q(owner=request.user)&Q(id=pot_id))
    tmpList = pot.user_list.all()
    print tmpList
    if request.method == 'POST':
        who_form = WhoForm(request.POST, request.FILES, instance=pot)
        if who_form.is_valid():
            who = who_form.save(commit=False)
            who_form.save()
            for item in tmpList:
                who.user_list.add(item)
            print tmpList
            return HttpResponseRedirect('/pots/'+str(pot_id)+'/who')
        else:
            print who_form.errors 
            return HttpResponseRedirect('/pots')
    else:
        who_form = WhoForm(instance=pot)
        return render_to_response('website/pot_who1.html', 
                                {'username': username,
                                'who_form': who_form,
                                'calendar_num_notifications': calendar_num_notifications,
                                'calendar_num_notif_zero':calendar_num_notif_zero,
                                'friend_num_notifications': friend_num_notifications,
                                'friend_num_notif_zero':friend_num_notif_zero,
                                'pot_num_notifications': pot_num_notifications,
                                'pot_num_notif_zero' : pot_num_notif_zero,
                                'pot': pot}, 
                                context_instance=RequestContext(request))

@login_required
def view_who2(request, pot_id):
    username = request.user.username

     #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    pot = Pot.objects.get(Q(owner=request.user)&Q(id=pot_id))

    user_friends = pot.who_for.friends

    tmpList = pot.user_list.all()
    print tmpList
    if request.method == 'POST':
        who_form = WhoForm(request.POST, request.FILES, instance=pot)
        if who_form.is_valid():
            who = who_form.save(commit=False)
            who_form.save()
            for item in tmpList:
                who.user_list.add(item)
            print tmpList
            return HttpResponseRedirect('/pots/'+str(pot_id)+'/who')
        else:
            print who_form.errors 
            return HttpResponseRedirect('/pots')
    else:
        who_form = WhoForm(instance=pot)
        return render_to_response('website/pot_who2.html', 
                                {'username': username,
                                'user_friends': user_friends,
                                'who_form': who_form,
                                'calendar_num_notifications': calendar_num_notifications,
                                'calendar_num_notif_zero':calendar_num_notif_zero,
                                'friend_num_notifications': friend_num_notifications,
                                'friend_num_notif_zero':friend_num_notif_zero,
                                'pot_num_notifications': pot_num_notifications,
                                'pot_num_notif_zero' : pot_num_notif_zero,
                                'pot': pot}, 
                                context_instance=RequestContext(request))

@login_required
def view_what(request, pot_id):
    username = request.user.username
    user = request.user.get_profile()
    pot = Pot.objects.get(Q(owner=request.user)&Q(id=pot_id))
    product_list = pot.product_list
    choices = Choice.objects.filter(pot=pot)
    
    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False

    return render_to_response('website/pot_what_open.html',
        {'username': username, 
        'product_list':product_list, 
        'pot':pot,
        'choices': choices,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero}, 
        context_instance=RequestContext(request))


def view_boutique(request):
    product_list = Product.objects.all()

    if request.user.is_authenticated():
        #fichajes block
        fichajes = request.user.get_profile().fichajes

        #notifications block
        calendar_num_notifications = notifications_count(request, 'calendar')
        friend_num_notifications = notifications_count(request, 'friend_request')
        pot_num_notifications = notifications_count(request, 'pot')
        if calendar_num_notifications == 0:
            calendar_num_notif_zero = True
        else:
            calendar_num_notif_zero = False

        if friend_num_notifications == 0:
            friend_num_notif_zero = True
        else:
            friend_num_notif_zero = False

        if pot_num_notifications == 0:
            pot_num_notif_zero = True
        else:
            pot_num_notif_zero = False
    else:
        calendar_num_notifications = 0
        friend_num_notifications = 0
        pot_num_notifications = 0
        calendar_num_notif_zero = True
        friend_num_notif_zero = True
        pot_num_notif_zero = True
        fichajes = 0



    return render_to_response('website/gift_boutique.html',
        {'product_list': product_list,
        'fichajes': fichajes,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero}, 
        context_instance=RequestContext(request))

@login_required
def view_fichajes(request):

    #fichajes block
    fichajes = request.user.get_profile().fichajes

    #notifications block
    calendar_num_notifications = notifications_count(request, 'calendar')
    friend_num_notifications = notifications_count(request, 'friend_request')
    pot_num_notifications = notifications_count(request, 'pot')
    if calendar_num_notifications == 0:
        calendar_num_notif_zero = True
    else:
        calendar_num_notif_zero = False

    if friend_num_notifications == 0:
        friend_num_notif_zero = True
    else:
        friend_num_notif_zero = False

    if pot_num_notifications == 0:
        pot_num_notif_zero = True
    else:
        pot_num_notif_zero = False



    return render_to_response('website/gift_fichajes.html',
        {'fichajes': fichajes,
        'calendar_num_notifications': calendar_num_notifications,
        'calendar_num_notif_zero':calendar_num_notif_zero,
        'friend_num_notifications': friend_num_notifications,
        'friend_num_notif_zero':friend_num_notif_zero,
        'pot_num_notifications': pot_num_notifications,
        'pot_num_notif_zero' : pot_num_notif_zero}, 
        context_instance=RequestContext(request))
