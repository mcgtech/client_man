from django.conf import settings
from templated_email import send_templated_mail
from .general import msg_once_only

def send_email_using_template(from_email, recipient_list, context, template, request):
    send_templated_mail(
        template_name=template,
        from_email=from_email,
        recipient_list=recipient_list,
        context=context,
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )
    msg_once_only(request, 'Email sent to ' + str(recipient_list), settings.SUCC_MSG_TYPE)