from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import datetime

from django.conf import settings
from django.db.models import signals

class Product(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(null=True, max_length=255)
    price = models.IntegerField(null=True, default=0)
    profile_image  = models.FileField(upload_to = 'profiles/', null=True, blank=True, default="profiles/Universidad_de_Deusto.jpg")
    date = models.DateField(auto_now_add=True)
    link = models.CharField(null=True, max_length=255)
    clicks = models.IntegerField(null=True, default=0)
    def __unicode__(self):
        return u'%s %s %d' % (self.name, self.price, self.clicks)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    first_name = models.CharField(max_length=30, default='Nombre')
    last_name = models.CharField(max_length=30)
    location = models.CharField(max_length=30, null=True)
    bday = models.DateField(null=True)
    profile_image  = models.FileField(upload_to = 'profiles/', null=True, blank=True, default="profiles/Universidad_de_Deusto.jpg")
    friends = models.ManyToManyField("self")
    fichajes = models.ManyToManyField(Product, related_name='user_fichajes')

    def __unicode__(self):
        # return u'%s %s %s' % (self.first_name, self.last_name, self.bday.date().strftime("%d-%m-%Y"))
        return u'%s %s' % (self.first_name, self.last_name)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

class FriendRequest(models.Model):
    STATUS_CHOICES = (
        (u'P', u'Pendent'),
        (u'R', u'Read'),
    )
    text = models.CharField(max_length=140)
    sender = models.ForeignKey(UserProfile, unique=False, related_name='request_sender')
    sender_username = models.CharField(max_length=140, null=True)
    receiver = models.ForeignKey(UserProfile, unique=False, related_name='request_receiver')
    receiver_username = models.CharField(max_length=140, null=True)
    date = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s to %s' % (self.sender, self.receiver)

class MessageThread(models.Model):
    date = models.DateField(auto_now_add=True)
    sender = models.ForeignKey('UserProfile', related_name='sender', null=True)
    receiver = models.ForeignKey('UserProfile', related_name='receiver', null=True)

class Message(models.Model):
    text = models.CharField(max_length=140)
    thread = models.ForeignKey(MessageThread)
    date = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s to %s' % (self.sender, self.receiver)

class DateType(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=140)
    def __unicode__(self):
        return u'%s' % (self.name)

class SpecialDate(models.Model):
    owner = models.ForeignKey(UserProfile, unique=False, related_name='special_date_owner')
    date_type = models.ForeignKey(DateType, unique=False, related_name='special_date_type')
    date = models.DateField(unique=False)
    def __unicode__(self):
        return u'%s de %s' % (self.date_type, self.owner)

class NotificationType(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=140)
    def __unicode__(self):
        return u'%s' % (self.name)

class Notification(models.Model):
    owner = models.ForeignKey(UserProfile, unique=False, related_name='notification_owner')
    notification_type = models.ForeignKey(NotificationType, unique=False, related_name='notification_type')
    def __unicode__(self):
        return u'%s de %s' % (self.notification_type, self.owner)

class Pot(models.Model):
    owner = models.ForeignKey(UserProfile, unique=False, related_name='pot_owner')
    user_list = models.ManyToManyField(UserProfile, related_name='pot_user_list')
    what_for = models.ForeignKey(DateType, unique=False, related_name='pot_what_for')
    who_for = models.ForeignKey(UserProfile, unique=False, related_name='pot_who_for')
    price = models.IntegerField(null=True, default=0)
    date = models.DateField(null=True)
    product_list = models.ManyToManyField(Product, blank=True, null=True, related_name='pot_product_list')
    is_paid = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s de %s' % (self.what_for, self.who_for)

    def getPotDetails(self):
        return u'%s de %s' % (self.what_for, self.who_for)

class Choice(models.Model):
    pot = models.ForeignKey(Pot, related_name='product_choice')
    product_choice = models.ForeignKey(Product, unique=False, related_name='product_choice')
    votes = models.IntegerField(null=True, default = 0)
    def __unicode__(self):
        return u'%s votes:%s' % (self.product_choice, self.votes)