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

from __future__ import absolute_import, division, print_function, unicode_literals
from django.db import models, migrations
import emails.models
import django.utils.timezone
import fluo.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(default=None, max_length=255, null=True, verbose_name='filename', blank=True)),
                ('content_base64', fluo.db.models.fields.Base64Field(default=None, null=True, verbose_name='content', db_column=b'content', blank=True)),
                ('mimetype', models.CharField(default=None, max_length=255, null=True, verbose_name='mimetype', blank=True)),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', fluo.db.models.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('last_modified_at', fluo.db.models.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('from_email', models.CharField(default=emails.models._get_default_from_email, max_length=255, verbose_name='from email')),
                ('to_emails', models.CharField(default='', max_length=255, verbose_name='to emails')),
                ('cc_emails', models.CharField(default='', max_length=255, verbose_name='cc emails')),
                ('bcc_emails', models.CharField(default='', max_length=255, verbose_name='bcc emails')),
                ('all_recipients', models.TextField(default='', verbose_name='recipients', blank=True)),
                ('headers', models.TextField(default='', verbose_name='headers', blank=True)),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body')),
                ('raw', models.TextField(default='', verbose_name='raw message', blank=True)),
            ],
            options={
                'verbose_name': 'email',
                'verbose_name_plural': 'emails',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', fluo.db.models.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('last_modified_at', fluo.db.models.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('from_email', models.CharField(default=emails.models._get_default_from_email, max_length=255, verbose_name='from email')),
                ('default_to', models.CharField(help_text='comma separated value', max_length=255, null=True, verbose_name='default to', blank=True)),
                ('default_cc', models.CharField(help_text='comma separated value', max_length=255, null=True, verbose_name='default cc', blank=True)),
                ('default_bcc', models.CharField(help_text='comma separated value', max_length=255, null=True, verbose_name='default bcc', blank=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name', db_index=True)),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body')),
                ('body_html', models.TextField(default='', verbose_name='html body', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'email template',
                'verbose_name_plural': 'email templates',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplateTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(db_index=True, max_length=5, verbose_name='language', choices=[('it', 'Italian'), ('en', 'English')])),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body')),
                ('body_html', models.TextField(default='', verbose_name='body', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', verbose_name='parent', to='emails.EmailTemplate')),
            ],
            options={
                'verbose_name': 'mail translation',
                'verbose_name_plural': 'mail translations',
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='email',
            field=models.ForeignKey(related_name='attachments', verbose_name='email', to='emails.Email'),
        ),
        migrations.AlterUniqueTogether(
            name='emailtemplatetranslation',
            unique_together=set([('language', 'parent')]),
        ),
    ]
