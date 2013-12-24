# -*- coding: utf-8 -*-

# Copyright (C) 2007-2013, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailTemplate'
        db.create_table(u'emails_emailtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('fluo.db.models.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('last_modified_at', self.gf('fluo.db.models.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('from_email', self.gf('django.db.models.fields.CharField')(default=u'Gnammo <info@gnammo.com>', max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'emails', ['EmailTemplate'])

        # Adding model 'EmailTemplateTranslation'
        db.create_table(u'emails_emailtemplatetranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'translations', to=orm['emails.EmailTemplate'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'emails', ['EmailTemplateTranslation'])

        # Adding unique constraint on 'EmailTemplateTranslation', fields ['language', 'parent']
        db.create_unique(u'emails_emailtemplatetranslation', ['language', 'parent_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'EmailTemplateTranslation', fields ['language', 'parent']
        db.delete_unique(u'emails_emailtemplatetranslation', ['language', 'parent_id'])

        # Deleting model 'EmailTemplate'
        db.delete_table(u'emails_emailtemplate')

        # Deleting model 'EmailTemplateTranslation'
        db.delete_table(u'emails_emailtemplatetranslation')


    models = {
        u'emails.emailtemplate': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'EmailTemplate'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('fluo.db.models.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'default': "u'Gnammo <info@gnammo.com>'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_at': ('fluo.db.models.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'emails.emailtemplatetranslation': {
            'Meta': {'unique_together': "((u'language', u'parent'),)", 'object_name': 'EmailTemplateTranslation'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'translations'", 'to': u"orm['emails.EmailTemplate']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['emails']
