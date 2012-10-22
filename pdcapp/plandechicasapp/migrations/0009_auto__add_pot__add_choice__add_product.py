# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pot'
        db.create_table('plandechicasapp_pot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pot_owner', to=orm['plandechicasapp.UserProfile'])),
            ('what_for', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pot_what_for', to=orm['plandechicasapp.DateType'])),
            ('who_for', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pot_who_for', to=orm['plandechicasapp.UserProfile'])),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('is_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_purchased', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('plandechicasapp', ['Pot'])

        # Adding M2M table for field user_list on 'Pot'
        db.create_table('plandechicasapp_pot_user_list', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pot', models.ForeignKey(orm['plandechicasapp.pot'], null=False)),
            ('userprofile', models.ForeignKey(orm['plandechicasapp.userprofile'], null=False))
        ))
        db.create_unique('plandechicasapp_pot_user_list', ['pot_id', 'userprofile_id'])

        # Adding M2M table for field product_list on 'Pot'
        db.create_table('plandechicasapp_pot_product_list', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pot', models.ForeignKey(orm['plandechicasapp.pot'], null=False)),
            ('product', models.ForeignKey(orm['plandechicasapp.product'], null=False))
        ))
        db.create_unique('plandechicasapp_pot_product_list', ['pot_id', 'product_id'])

        # Adding model 'Choice'
        db.create_table('plandechicasapp_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pot', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product_choice', to=orm['plandechicasapp.Pot'])),
            ('product_choice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product_choice', to=orm['plandechicasapp.Product'])),
            ('votes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('plandechicasapp', ['Choice'])

        # Adding model 'Product'
        db.create_table('plandechicasapp_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('profile_image', self.gf('django.db.models.fields.files.FileField')(default='profiles/Universidad_de_Deusto.jpg', max_length=100, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('clicks', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('plandechicasapp', ['Product'])


    def backwards(self, orm):
        # Deleting model 'Pot'
        db.delete_table('plandechicasapp_pot')

        # Removing M2M table for field user_list on 'Pot'
        db.delete_table('plandechicasapp_pot_user_list')

        # Removing M2M table for field product_list on 'Pot'
        db.delete_table('plandechicasapp_pot_product_list')

        # Deleting model 'Choice'
        db.delete_table('plandechicasapp_choice')

        # Deleting model 'Product'
        db.delete_table('plandechicasapp_product')


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
        'plandechicasapp.choice': {
            'Meta': {'object_name': 'Choice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_choice'", 'to': "orm['plandechicasapp.Pot']"}),
            'product_choice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_choice'", 'to': "orm['plandechicasapp.Product']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        },
        'plandechicasapp.datetype': {
            'Meta': {'object_name': 'DateType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
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
        'plandechicasapp.notification': {
            'Meta': {'object_name': 'Notification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_type'", 'to': "orm['plandechicasapp.NotificationType']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_owner'", 'to': "orm['plandechicasapp.UserProfile']"})
        },
        'plandechicasapp.notificationtype': {
            'Meta': {'object_name': 'NotificationType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'plandechicasapp.pot': {
            'Meta': {'object_name': 'Pot'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_purchased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pot_owner'", 'to': "orm['plandechicasapp.UserProfile']"}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'product_list': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pot_product_list'", 'symmetrical': 'False', 'to': "orm['plandechicasapp.Product']"}),
            'user_list': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pot_user_list'", 'symmetrical': 'False', 'to': "orm['plandechicasapp.UserProfile']"}),
            'what_for': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pot_what_for'", 'to': "orm['plandechicasapp.DateType']"}),
            'who_for': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pot_who_for'", 'to': "orm['plandechicasapp.UserProfile']"})
        },
        'plandechicasapp.product': {
            'Meta': {'object_name': 'Product'},
            'clicks': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'profile_image': ('django.db.models.fields.files.FileField', [], {'default': "'profiles/Universidad_de_Deusto.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'plandechicasapp.specialdate': {
            'Meta': {'object_name': 'SpecialDate'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'special_date_type'", 'to': "orm['plandechicasapp.DateType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'special_date_owner'", 'to': "orm['plandechicasapp.UserProfile']"})
        },
        'plandechicasapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "'Nombre'", 'max_length': '30'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'to': "orm['plandechicasapp.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'profile_image': ('django.db.models.fields.files.FileField', [], {'default': "'profiles/Universidad_de_Deusto.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['plandechicasapp']