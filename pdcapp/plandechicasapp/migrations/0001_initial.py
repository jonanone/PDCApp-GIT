# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('plandechicasapp_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='Nombre', max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('bday', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('plandechicasapp', ['UserProfile'])

        # Adding M2M table for field friends on 'UserProfile'
        db.create_table('plandechicasapp_userprofile_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm['plandechicasapp.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm['plandechicasapp.userprofile'], null=False))
        ))
        db.create_unique('plandechicasapp_userprofile_friends', ['from_userprofile_id', 'to_userprofile_id'])

        # Adding model 'FriendRequest'
        db.create_table('plandechicasapp_friendrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='request_sender', to=orm['plandechicasapp.UserProfile'])),
            ('sender_username', self.gf('django.db.models.fields.CharField')(max_length=140, null=True)),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='request_receiver', to=orm['plandechicasapp.UserProfile'])),
            ('receiver_username', self.gf('django.db.models.fields.CharField')(max_length=140, null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('plandechicasapp', ['FriendRequest'])

        # Adding model 'MessageThread'
        db.create_table('plandechicasapp_messagethread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', null=True, to=orm['plandechicasapp.UserProfile'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', null=True, to=orm['plandechicasapp.UserProfile'])),
        ))
        db.send_create_signal('plandechicasapp', ['MessageThread'])

        # Adding model 'Message'
        db.create_table('plandechicasapp_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plandechicasapp.MessageThread'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('plandechicasapp', ['Message'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('plandechicasapp_userprofile')

        # Removing M2M table for field friends on 'UserProfile'
        db.delete_table('plandechicasapp_userprofile_friends')

        # Deleting model 'FriendRequest'
        db.delete_table('plandechicasapp_friendrequest')

        # Deleting model 'MessageThread'
        db.delete_table('plandechicasapp_messagethread')

        # Deleting model 'Message'
        db.delete_table('plandechicasapp_message')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'plandechicasapp.friendrequest': {
            'Meta': {'object_name': 'FriendRequest'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'request_receiver'", 'to': "orm['plandechicasapp.UserProfile']"}),
            'receiver_username': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'request_sender'", 'to': "orm['plandechicasapp.UserProfile']"}),
            'sender_username': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'plandechicasapp.message': {
            'Meta': {'object_name': 'Message'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plandechicasapp.MessageThread']"})
        },
        'plandechicasapp.messagethread': {
            'Meta': {'object_name': 'MessageThread'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'null': 'True', 'to': "orm['plandechicasapp.UserProfile']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'null': 'True', 'to': "orm['plandechicasapp.UserProfile']"})
        },
        'plandechicasapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "'Nombre'", 'max_length': '30'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'to': "orm['plandechicasapp.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['plandechicasapp']