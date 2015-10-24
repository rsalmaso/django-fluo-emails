# -*- coding: utf-8 -*-

# Copyright (C) 2007-2015, Raffaele Salmaso <raffaele@salmaso.org>
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(null=True, default=None, max_length=255, blank=True, verbose_name='filename')),
                ('content', models.BinaryField(blank=True, null=True, default=None, verbose_name='content')),
                ('mimetype', models.CharField(null=True, default=None, max_length=255, blank=True, verbose_name='mimetype')),
            ],
            options={
                'verbose_name_plural': 'attachments',
                'verbose_name': 'attachment',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_at', fluo.db.models.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('last_modified_at', fluo.db.models.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='modified', editable=False)),
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
                'verbose_name_plural': 'emails',
                'verbose_name': 'email',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_at', fluo.db.models.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('last_modified_at', fluo.db.models.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('from_email', models.CharField(default=emails.models._get_default_from_email, max_length=255, verbose_name='from email')),
                ('default_to', models.CharField(verbose_name='default to', null=True, help_text='comma separated value', blank=True, max_length=255)),
                ('default_cc', models.CharField(verbose_name='default cc', null=True, help_text='comma separated value', blank=True, max_length=255)),
                ('default_bcc', models.CharField(verbose_name='default bcc', null=True, help_text='comma separated value', blank=True, max_length=255)),
                ('name', models.CharField(db_index=True, unique=True, max_length=255, verbose_name='name')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body')),
                ('body_html', models.TextField(default='', verbose_name='html body', blank=True)),
            ],
            options={
                'verbose_name_plural': 'email templates',
                'verbose_name': 'email template',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EmailTemplateTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(db_index=True, max_length=5, choices=[('en', 'English'), ('it', 'Italian')], verbose_name='language')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body')),
                ('body_html', models.TextField(default='', verbose_name='body', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', verbose_name='parent', to='emails.EmailTemplate')),
            ],
            options={
                'verbose_name_plural': 'mail translations',
                'verbose_name': 'mail translation',
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
