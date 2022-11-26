"""
utility file for sending mail and other
"""


import multitasking
from typing import List

from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags


@multitasking.task
def send_email(subject: str, html_message: str, recipient_list: List[str]) -> None:
    """send mail to user using multitasking

    Arguments:
        subject {str} -- subject of the mail
        html_message {str} -- html message to sending (after render_to_string in view)
        recipient_list {List[str]} -- list of recipient email
    """

    plain_message = strip_tags(html_message)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        html_message=html_message,
    )
