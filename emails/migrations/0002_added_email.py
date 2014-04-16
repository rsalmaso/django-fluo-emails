# -*- coding: utf-8 -*-

# Copyright (C) 2007-2014, Raffaele Salmaso <raffaele@salmaso.org>
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

from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table(u'emails_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('fluo.db.models.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('last_modified_at', self.gf('fluo.db.models.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('from_email', self.gf('django.db.models.fields.CharField')(default=u'Gnammo <info@gnammo.com>', max_length=255)),
            ('to_emails', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            ('cc_emails', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            ('bcc_emails', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            ('all_recipients', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('headers', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('raw', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal(u'emails', ['Email'])

        # Adding model 'Attachment'
        db.create_table(u'emails_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'attachments', to=orm['emails.Email'])),
            ('filename', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('content_base64', self.gf('fluo.db.models.fields.Base64Field')(default=None, null=True, db_column='content', blank=True)),
            ('mimetype', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'emails', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table(u'emails_email')

        # Deleting model 'Attachment'
        db.delete_table(u'emails_attachment')


    models = {
        u'emails.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'content_base64': ('fluo.db.models.fields.Base64Field', [], {'default': 'None', 'null': 'True', 'db_column': "'content'", 'blank': 'True'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'attachments'", 'to': u"orm['emails.Email']"}),
            'filename': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'emails.email': {
            'Meta': {'object_name': 'Email'},
            'all_recipients': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'bcc_emails': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'cc_emails': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'created_at': ('fluo.db.models.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'default': "u'Gnammo <info@gnammo.com>'", 'max_length': '255'}),
            'headers': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_at': ('fluo.db.models.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'raw': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'to_emails': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'})
        },
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
