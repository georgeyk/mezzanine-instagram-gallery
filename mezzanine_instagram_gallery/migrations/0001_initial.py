# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InstagramUser'
        db.create_table('mezzanine_instagram_gallery_instagramuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instagram_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('mezzanine_instagram_gallery', ['InstagramUser'])

        # Adding model 'InstagramMedia'
        db.create_table('mezzanine_instagram_gallery_instagrammedia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instagram_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('comment_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('like_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('thumbnail_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('standard_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('downloaded', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mezzanine_instagram_gallery', ['InstagramMedia'])


    def backwards(self, orm):
        # Deleting model 'InstagramUser'
        db.delete_table('mezzanine_instagram_gallery_instagramuser')

        # Deleting model 'InstagramMedia'
        db.delete_table('mezzanine_instagram_gallery_instagrammedia')


    models = {
        'mezzanine_instagram_gallery.instagrammedia': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'InstagramMedia'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'like_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'standard_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'mezzanine_instagram_gallery.instagramuser': {
            'Meta': {'object_name': 'InstagramUser'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['mezzanine_instagram_gallery']