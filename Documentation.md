### Инструкция по запуску приложения:
1. Создать и настроить .env по пути ./app/.env
```
DEBUG=1
SECRET_KEY='SECRET_KEY'
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_PASSWORD='password'
POSTGRES_PORT='port'
```
2. docker-compose build
3. docker-compose up -d
4. docker exec -it "Container ID" bash
5. su - postgres
6. createdb diplom_db
7. docker-compose exec web python manage.py migrate
8. docker-compose exec web python manage.py createsuperuser
- Необходимые Docker file настроены!
  
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
