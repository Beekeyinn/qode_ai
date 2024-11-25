from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_mail_function(reciever, subject, message, *args, **kwargs):
    print("send_mail_function: ", reciever, subject, message)
    _html = get_template("email/email.html").render(
        {"subject": subject, "message": message}
    )
    _text = get_template("email/email.txt").render(
        {"subject": subject, "message": message}
    )
    try:
        msg = EmailMultiAlternatives(
            subject, _text, getattr(settings, "DEFAULT_FROM_EMAIL_HOST"), [reciever]
        )
        msg.attach_alternative(_html, "text/html")
        msg.send(fail_silently=False)
    except Exception as e:
        return {
            "success": False,
            "message": "Failed to send email",
            "exception": f"{e}",
        }
    else:
        return {"success": True, "message": "Successfully Sent"}
