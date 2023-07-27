from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def new_post_for_send(instance):
    template = 'mail/post_for_send.html'
    for category in instance.category.all():
        for user in category.subscribers.all():
            html_content = render_to_string('mail/post_for_send.html', {'new_post': instance, 'user': user})
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.text,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()