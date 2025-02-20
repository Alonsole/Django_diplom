from typing import Type

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created

from .models import ConfirmEmailToken, User

new_user_registered = Signal()

new_order = Signal()


@shared_task
def send_password_reset_token_email(user_email, token_key):
    """
    Отправляем письмо с токеном для сброса пароля
    """
    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {user_email}",
        # message:
        token_key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user_email]
    )
    msg.send()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Запускаем асинхронную задачу для отправки письма с токеном для сброса пароля
    """
    send_password_reset_token_email.delay(reset_password_token.user.email, reset_password_token.key)


@shared_task
def send_confirmation_email(user_email, token_key):
    """
    Отправляем письмо с подтверждением почты
    """
    msg = EmailMultiAlternatives(
        # title:
        f"Email Confirmation Token for {user_email}",
        # message:
        token_key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user_email]
    )
    msg.send()


@receiver(post_save, sender=User)
def new_user_registered_signal(sender: Type[User], instance: User, created: bool, **kwargs):
    """
    Запускаем асинхронную задачу для отправки письма с подтверждением почты
    """
    if created and not instance.is_active:
        token, _ = ConfirmEmailToken.objects.get_or_create(user_id=instance.pk)
        send_confirmation_email.delay(instance.email, token.key)


@shared_task
def send_order_email(user_id, order_id, status):
    """
    Отправляем письмо при изменении статуса заказа
    Словарь для преобразования статуса заказа в текстовое сообщение на русском языке
    """
    user = User.objects.get(id=user_id)
    order = Order.objects.get(id=order_id)

    status_messages = {'confirmed': 'Подтвержден',
                       'assembled': 'Собран',
                       'sent': 'Отправлен',
                       'delivered': 'Доставлен',
                       'canceled': 'Отменен'}

    subject = f"Обновление статуса заказа №{order.id}"  # Тема сообщения
    message = f'Статус вашего заказа №{order_id} изменен на "{status_messages[status]}"'  # Текст сообщения

    msg = EmailMultiAlternatives(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()
