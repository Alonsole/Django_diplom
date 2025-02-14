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


