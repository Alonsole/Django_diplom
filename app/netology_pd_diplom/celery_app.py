import os
import django
from celery import Celery
from celery.result import AsyncResult
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

# Инициализация Django для скриптов вне основного процесса сервера
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netology_pd_diplom.settings')
django.setup()

# Создание экземпляра Celery и автоматическое обнаружение задач
celery_app = Celery('celery_app_for_pyhon_diplom')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


@celery_app.task
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )


@celery_app.task
def do_import():
    # логика импорта
    pass


# Функция для получения статуса и результата задачи
def get_task(task_id: str) -> AsyncResult:
    """
    Получение результата выполнения асинхронной задачи Celery по её идентификатору.

    :param task_id: Идентификатор задачи
    :return: Объект AsyncResult, содержащий информацию о статусе и результате выполнения задачи
    """
    return AsyncResult(task_id, app=celery_app)


def test_email_view(request):
    """
    Отправка тестового письма с использованием Celery.
    """
    task = send_email.delay(
        subject="Test Celery Email",
        message="Это тестовое письмо Celery",
        recipient_list=[os.getenv("TestMail")]
    )

    return JsonResponse({"task_id": task.id, "status": "Email task created"})
