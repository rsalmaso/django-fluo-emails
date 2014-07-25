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

# Email/Attachment adapted from https://github.com/stefanfoulis/django-database-email-backend
# Copyright (C) 2011 Stefan Foulis and contributors.

from __future__ import absolute_import, division, print_function, unicode_literals
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Template, RequestContext, Context
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.sites.models import Site
from fluo.db import models


def _get_default_from_email():
    return settings.DEFAULT_FROM_EMAIL


class EmailTemplateManager(models.Manager):
    def send(self, name, request, to=None, cc=None, bcc=None, context=None, fail_silently=True):
        mail = self.get(name=name)
        mail.send(
            request=request,
            to=to,
            cc=cc,
            bcc=bcc,
            context=context,
            fail_silently=fail_silently,
        )


@python_2_unicode_compatible
class EmailTemplate(models.TimestampModel, models.I18NModel):
    objects = EmailTemplateManager()

    from_email = models.CharField(
        max_length=255,
        default=_get_default_from_email,
        verbose_name=_('from email'),
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name=_('name'),
    )
    subject = models.CharField(
        max_length=255,
        verbose_name=_('subject'),
    )
    body = models.TextField(
        verbose_name=_('body'),
    )
    body_html = models.TextField(
        blank=True,
        default='',
        verbose_name=_('html body'),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('email template')
        verbose_name_plural = _('email templates')

    def __str__(self):
        return self.name

    def send(self, request=None, to=None, cc=None, bcc=None, context=None, fail_silently=True):
        site = Site.objects.get_current()
        subject_template = Template(self.subject)
        body_template = Template(self.body)

        context = {} if context is None else context
        context = Context(context) if request is None else RequestContext(request, context)

        subject = subject_template.render(context)
        body = body_template.render(context)

        if isinstance(to, basestring):
            to = [ to ]
        if isinstance(cc, basestring):
            cc = [ cc ]
        if isinstance(bcc, basestring):
            bcc = [ bcc ]

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=self.from_email,
            to=to,
            cc=cc,
            bcc=bcc,
            headers={
                'Reply-to': 'noreply@%s' % site.domain,
            },
        )
        email.send(fail_silently=fail_silently)


@python_2_unicode_compatible
class EmailTemplateTranslation(models.TranslationModel):
    parent = models.ForeignKey(
        EmailTemplate,
        related_name='translations',
        verbose_name=_('parent'),
    )
    subject = models.CharField(
        max_length=255,
        verbose_name=_('subject'),
    )
    body = models.TextField(
        verbose_name=_('body'),
    )
    body_html = models.TextField(
        blank=True,
        default='',
        verbose_name=_('body'),
    )

    class Meta:
        unique_together = (('language', 'parent',),)
        verbose_name = _('mail translation')
        verbose_name_plural = _('mail translations')

    def __str__(self):
        return "%(name)s [%(lang)s]" % {
            'name': self.parent.name,
            'lang': self.language[:2],
        }


@python_2_unicode_compatible
class Email(models.TimestampModel):
    from_email = models.CharField(
        max_length=255,
        default=_get_default_from_email,
        verbose_name=_('from email'),
    )
    to_emails = models.CharField(
        max_length=255,
        default='',
        verbose_name=_('to emails'),
    )
    cc_emails = models.CharField(
        max_length=255,
        default='',
        verbose_name=_('cc emails'),
    )
    bcc_emails = models.CharField(
        max_length=255,
        default='',
        verbose_name=_('bcc emails'),
    )
    all_recipients = models.TextField(
        blank=True,
        default='',
        verbose_name=_('recipients'),
    )
    headers =  models.TextField(
        blank=True,
        default='',
        verbose_name=_('headers'),
    )
    subject = models.CharField(
        max_length=255,
        verbose_name=_('subject'),
    )
    body = models.TextField(
        verbose_name=_('body'),
    )
    raw = models.TextField(
        blank=True,
        default='',
        verbose_name=_('raw message'),
    )

    class Meta:
        #ordering = ('name',)
        verbose_name = _('email')
        verbose_name_plural = _('emails')

    def __str__(self):
        return _('Email from "%(from_email)s" to "%(to_emails)s" sent at %(sent_at)s about "%(subject)s"') % {
            'from_email': self.from_email,
            'to_emails': self.to_emails,
            'sent_at': self.created_at,
            'subject': self.subject,
        }

    @property
    def attachment_count(self):
        if not hasattr(self, 'attachment_count_cache'):
            self.attachment_count_cache = self.attachments.count()
        return self.attachment_count_cache


class Attachment(models.Model):
    email = models.ForeignKey(
        Email,
        related_name='attachments',
        verbose_name=_('email'),
    )
    filename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        verbose_name=_('filename'),
    )
    content = models.Base64Field(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('content'),
    )
    mimetype = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        verbose_name=_('mimetype'),
    )

    class Meta:
        #ordering = ('name',)
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')
