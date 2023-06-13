from __future__ import unicode_literals

from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_from_template(to_email, from_email, subject,
                             markdown_template=None,
                             text_template=None, html_template=None,
                             fail_silently=False, context=None,
                             **kwargs):
    """Send an email from a template.

    :param to_email: the email address to send the email to
    :param from_email: the email address the email will be from
    :param subject: the subject of the email
    :param markdown_template: the markdown syntax template to use for the
        email. If provided, this will generate both the text and html versions
        of the email. You must have the "markdown" library installed in order
        to use this. pip install markdown.
    :param text_template: the template for the text version of the email. This
        can be omitted if the markdown_template is provided.
    :param html_template: the template for the html version of the email. This
        can be omitted if the markdown_template is provided.
    :param context: the context for the email templates
    """
    return send_emails_from_template(
        to_emails=[to_email],
        from_email=from_email,
        subject=subject,
        markdown_template=markdown_template,
        text_template=text_template,
        html_template=html_template,
        fail_silently=fail_silently,
        context=context,
        **kwargs
    )


def send_emails_from_template(to_emails, from_email, subject,
                              markdown_template=None, text_template=None,
                              html_template=None, fail_silently=False,
                              context=None, attachments=None, **kwargs):
    """Send many emails from single template.  Each email address listed in the
    ``to_emails`` will receive an separate email.

    :param to_emails: list of email address to send the email to
    :param from_email: the email address the email will be from
    :param subject: the subject of the email
    :param markdown_template: the markdown syntax template to use for the
        email.  If provided, this will generate both the text and html versions
        of the email. You must have the "markdown" library installed in order
        to use this. pip install markdown.
    :param text_template: the template for the text version of the email. This
        can be omitted if the markdown_template is provided.
    :param html_template: the template for the html version of the email. This
        can be omitted if the markdown_template is provided.
    :param context: the context for the email templates
    :param attachments: list of additional attachments to add to the email
        (example: email.mime.image.MIMEImage object).  The attachments will be
        added to each email sent.
    """
    if not to_emails:
        return

    if context is None:
        context = {}

    if markdown_template:
        try:
            from markdown import markdown
        except ImportError:
            raise ImportError(
                'The application is attempting to send an email by using the '
                '"markdown" library, but markdown is not installed.  Please '
                'install it. See: '
                'http://pythonhosted.org/Markdown/install.html'
            )

        base_html_template = getattr(settings,
                                     'CORE_BASE_HTML_EMAIL_TEMPLATE',
                                     'django_core/mail/base_email.html')

        text_content = render_to_string(markdown_template, context)
        context['email_content'] = markdown(text_content)
        html_content = render_to_string(base_html_template, context)
    else:
        text_content = render_to_string(text_template, context)
        html_content = render_to_string(html_template, context)

    emails = []

    for email_address in to_emails:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[email_address],
            alternatives=[(html_content, 'text/html')]
        )

        if attachments:
            email.mixed_subtype = 'related'

            for attachment in attachments:
                email.attach(attachment)

        emails.append(email)

    connection = mail.get_connection()

    connection.open()
    connection.send_messages(emails)
    connection.close()
