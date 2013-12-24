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

from __future__ import absolute_import, division, print_function, unicode_literals
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Template, RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from fluo.db import models
User = get_user_model()


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

    class Meta:
        ordering = ('name',)
        verbose_name = _('email template')
        verbose_name_plural = _('email templates')

    def __str__(self):
        return self.name

    def send(self, request, to=None, cc=None, bcc=None, context=None, fail_silently=True):
        site = Site.objects.get_current()
        subject_template = Template(self.subject)
        body_template = Template(self.body)

        context = {} if context is None else context
        context = RequestContext(request, context)

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

    class Meta:
        unique_together = (('language', 'parent',),)
        verbose_name = _('mail translation')
        verbose_name_plural = _('mail translations')

    def __str__(self):
        return "%(name)s [%(lang)s]" % {
            'name': self.parent.name,
            'lang': self.language[:2],
        }


