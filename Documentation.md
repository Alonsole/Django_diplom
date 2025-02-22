### Клонируйте репозиторий моего проекта
```
git clone git@github.com:Alonsole/Django_diplom.git
```

### Инструкция по запуску приложения:
1. Создать и настроить .env по пути ./app/.env
- Образец env файла предоставлен в проекте. 
```
DEBUG=1
SECRET_KEY='SECRET_KEY'
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_PASSWORD='password'
POSTGRES_PORT='port'
E_Password='Пароль для почты'
Email='Почтовый адрес для отправки писем'
TestMail='Адрес для отправки тестового письма Celery'
```
2. docker-compose build
3. docker-compose up -d
4. docker exec -it "Container ID db-1" bash
5. su - postgres
6. createdb diplom_db
  6.1. exit (выйти из контенера)
8. docker-compose exec web python manage.py migrate
9. docker-compose exec web python manage.py createsuperuser
- Необходимые Docker file настроены!
10. Проверьте запуск контейнеров и перейдите по адресу http://localhost/admin/
- Статику загружена и не требует повторной загрузки. 
## Структура проекта

- `app/`: Основной код приложения
  - `backend/`: Логика backend'а
 - `models.py`: Модели данных
 - `views.py`: Представления API
 - `serializers.py`: Сериализаторы для API
 - `urls.py`: URL-маршруты
  - `netology_pd_diplom/`: Настройки проекта
 - `settings.py`: Настройки Django
 - `celery_app.py`: Настройки Celery
- `nginx/`: Конфигурация Nginx
- `docker-compose.yml`: Конфигурация Docker

## API Endpoints

- `/api/user/register/` (POST): Регистрация нового пользователя
- `/api/user/login/` (POST): Вход пользователя
- `/api/user/confirm/` (POST): Подтверждение email пользователя
- `/api/shop/` (GET): Получение списка магазинов
- `/api/categories/` (GET): Получение списка категорий
- `/api/products/` (GET): Получение списка продуктов
- `/api/basket/` (GET, POST, PUT, DELETE): Управление корзиной пользователя
- `/api/order/` (GET, POST, PUT): Управление заказами

### Описание функций и скриптов проекта
1.`manage.py`:  
Основной скрипт для взаимодействия с Django. Используется для выполнения команд, таких как миграции базы данных, запуск сервера разработки и создание суперпользователя.  
2.`celery_app.py`:  
Инициализирует Celery и определяет задачи, которые могут выполняться асинхронно.  
Функция `send_email`: Асинхронно отправляет электронные письма с использованием настроек Django.  
Функция `do_import`: Заготовка для логики импорта данных (логика импорта должна быть реализована).  
Функция `get_task`: Возвращает статус и результат выполнения задачи Celery по её идентификатору.  
Функция `test_email_view`: Django view для отправки тестового письма с использованием Celery.  
3.`docker-compose.yml`:  
Определяет конфигурацию для запуска нескольких контейнеров Docker, включая веб-приложение, базу данных и Celery.
4.`Dockerfile`:  
Содержит инструкции для сборки Docker-образа вашего приложения. Включает установку зависимостей и настройку окружения.  
5.`settings.py`:  
Файл конфигурации Django, где определяются настройки проекта, такие как базы данных, установленные приложения, параметры безопасности и другие.  
6.`views.py`, `models.py`, `urls.py`:  
`views.py`: Логика обработки HTTP-запросов и возвращает соответствующие HTTP-ответы.  
`models.py`: Структура данных и взаимодействие с базой данных.  
`urls.py`: Маршрутизация URL-адресов к соответствующим представлениям.  
7.`requirements.txt`:  
Список зависимостей, необходимых для работы проекта.  
8. `signals.py`:  
Отправка уведомлений по событиям  
9. `admin.py`:  
Административная панель проекта  
