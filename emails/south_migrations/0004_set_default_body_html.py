# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        EmailTemplate = orm['emails.emailtemplate']

        for template in EmailTemplate.objects.all():
            template.body_html = ''
            template.save()

    def backwards(self, orm):
        pass

    models = {
        u'emails.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'content': ('fluo.db.models.fields.Base64Field', [], {'default': 'None', 'null': 'True', 'db_column': "'content'", 'blank': 'True'}),
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
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'translations'", 'to': u"orm['emails.EmailTemplate']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['emails']
