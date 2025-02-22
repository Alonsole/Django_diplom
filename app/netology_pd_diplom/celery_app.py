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
def update_partner_info(url, user_id):
    from django.core.exceptions import ValidationError
    from django.core.validators import URLValidator
    from requests import get
    from backend.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter
    from yaml import load as load_yaml, Loader

    validate_url = URLValidator()
    try:
        validate_url(url)
        stream = get(url).content
        data = load_yaml(stream, Loader=Loader)

        shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=user_id)
        for category in data['categories']:
            category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
            category_object.shops.add(shop.id)
            category_object.save()
        ProductInfo.objects.filter(shop_id=shop.id).delete()
        for item in data['goods']:
            product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

            product_info = ProductInfo.objects.create(product_id=product.id,
                                                      external_id=item['id'],
                                                      model=item['model'],
                                                      price=item['price'],
                                                      price_rrc=item['price_rrc'],
                                                      quantity=item['quantity'],
                                                      shop_id=shop.id)
            for name, value in item['parameters'].items():
                parameter_object, _ = Parameter.objects.get_or_create(name=name)
                ProductParameter.objects.create(product_info_id=product_info.id,
                                                parameter_id=parameter_object.id,
                                                value=value)
        return {'Status': True}
    except ValidationError as e:
        return {'Status': False, 'Error': str(e)}
    except Exception as e:
        return {'Status': False, 'Error': str(e)}


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
