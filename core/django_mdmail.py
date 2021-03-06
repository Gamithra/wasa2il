# django_mdmail
# Version: 0.3
# Authors: Helgi Hrafn Gunnarsson <helgi@binary.is>
# Repository: https://github.com/binary-is/django_mdmail
# License: MIT
#
# Description: django_mdmail bridges the gap between the `mdmail` package and
# Django. `mdmail` is a Python module that allows the sending of Markdown
# email. Django is a web development framework which contains its own wrapper
# functions for sending email. This package is a simple wrapper for `mdmail`
# utilizing Django's email settings and imitating Django's email function
# signature. Ideally, a Django user should be able to replace...
#
#     from django.core.mail import send_mail
#
# ...with...
#
#     from django_mdmail import send_mail
#
# ...to send Markdown emails with all the features of `mdmail`.
#
# Installation: This package is a single file with all the necessary
# information provided in comments at the top. To install or upgrade, simply
# place this file wherever you wish, import the `send_mail` function as
# described above and use it according to Django's documentation.
#
# You will need to have these Python packages installed: mdmail django
#
# Note: The parameter `html_message` can be used to override the HTML
# generated from Markdown but this feature should only be used under special
# circumstances because it defies the whole point of using `django_mdmail` in
# the first place.
#
# A function is also provided for processing *.md files into *.txt and *.html
# in Django's template directories, for use with built-in functionality like
# Django's forgotten-password mechanism. Run the function from some Django
# app's ready() hook (see AppConfig.ready() in Django documentation) and
# you'll only need to provide a Markdown version of those emails. Note that
# you may still have to do some coding of your own to make sure that both text
# and HTML emails are being sent (as opposed to only text emails).
#
# Limitations:
# * No inline images in email templates created by `convert_md_templates`.

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage
from mdmail import EmailContent

import os


# Warning to be placed in generated text and HTML files.
OVERRIDE_WARNING = 'WARNING! THIS FILE IS AUTO-GENERATED by django_mdmail upon Django startup. Changes to this file WILL be overwritten. In the same directory, there should be a file with the same name, except an ".md" ending (for Markdown). Edit that instead and restart Django.'


def send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None):

    # Have `mdmail` do its Markdown magic.
    content = EmailContent(message)

    # Create the email message and fill it with the relevant data.
    email = EmailMultiAlternatives(
        subject,
        content.text,
        from_email,
        recipient_list
    )
    email.attach_alternative(html_message or content.html, 'text/html')
    email.mixed_subtype = 'related'

    for filename, data in content.inline_images:
        # Create the image from the image data.
        image = MIMEImage(data.read())

        # Give the image an ID so that it can be found via HTML.
        image.add_header('Content-ID', '<{}>'.format(filename))

        # This header allows users of some email clients (for example
        # Thunderbird) to view the images as attachments when displaying the
        # message as plaintext, without it interrupting those users who view
        # it as HTML.
        image.add_header(
            'Content-Disposition', 'attachment; filename=%s' % filename
        )

        # Attach the image.
        email.attach(image)

    # Finally, send the message.
    email.send(fail_silently)


def convert_md_templates():
    '''
    Scans template directories for .md files and generates text and
    email-client-friendly HTML files from them, intended for email use.

    Use with AppConfig.ready() hooks (see Django documentation) to run at
    Django startup.

    Example `core/apps.py` file:

        from django.apps import AppConfig

        from django_mdmail import convert_md_templates

        class CoreConfig(AppConfig):
            name = 'core'

            def ready(self):
                convert_md_templates()
    '''

    override_comment = '{%% comment %%}%s{%% endcomment %%}\n' % OVERRIDE_WARNING

    # Find all the template directories we'll need to process and put them
    # in a flat list.
    template_dirs = []
    for template_conf in settings.TEMPLATES:
        template_dirs += [d for d in template_conf['DIRS']]

    # Iterate the template directories.
    for template_dir in template_dirs:
        for root, subdirs, filenames in os.walk(template_dir):
            for filename in filenames:
                if filename[-3:] == '.md':
                    md_path = os.path.join(root, filename)
                    txt_path = '%s.txt' % md_path[:-3]
                    html_path = '%s.html' % md_path[:-3]

                    with open(md_path, 'r') as f:
                        md_content = f.read()
                        f.close()

                    # Generate email-client-friendly HTML.
                    content = EmailContent(md_content)

                    with open(txt_path, 'w') as f:
                        f.write(override_comment + content.text)
                        f.close()

                    with open(html_path, 'w') as f:
                        f.write(override_comment + content.html)
                        f.close()
