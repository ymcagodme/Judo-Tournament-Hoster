# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mat'
        db.create_table('members_mat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mat_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('members', ['Mat'])

        # Adding model 'Division'
        db.create_table('members_division', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Mat'], null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('weight', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('members', ['Division'])

        # Adding model 'Member'
        db.create_table('members_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('division', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Division'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dojo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('weight', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('check_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('members', ['Member'])

        # Adding model 'Match'
        db.create_table('members_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Mat'])),
            ('match_number', self.gf('django.db.models.fields.IntegerField')()),
            ('winner', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('members', ['Match'])

        # Adding M2M table for field competitors on 'Match'
        db.create_table('members_match_competitors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('match', models.ForeignKey(orm['members.match'], null=False)),
            ('member', models.ForeignKey(orm['members.member'], null=False))
        ))
        db.create_unique('members_match_competitors', ['match_id', 'member_id'])

    def backwards(self, orm):
        # Deleting model 'Mat'
        db.delete_table('members_mat')

        # Deleting model 'Division'
        db.delete_table('members_division')

        # Deleting model 'Member'
        db.delete_table('members_member')

        # Deleting model 'Match'
        db.delete_table('members_match')

        # Removing M2M table for field competitors on 'Match'
        db.delete_table('members_match_competitors')

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
        'members.division': {
            'Meta': {'object_name': 'Division'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Mat']", 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'members.mat': {
            'Meta': {'object_name': 'Mat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mat_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'members.match': {
            'Meta': {'object_name': 'Match'},
            'competitors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['members.Member']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Mat']"}),
            'match_number': ('django.db.models.fields.IntegerField', [], {}),
            'winner': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'members.member': {
            'Meta': {'object_name': 'Member'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'check_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Division']", 'null': 'True', 'blank': 'True'}),
            'dojo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['members']