## Дипломный проект профессии «Python-разработчик: расширенный курс»
### Backend-приложение для автоматизации закупок
Приложение предназначено для автоматизации закупок в розничной сети через REST API.

**Пользователи сервиса:**

1. Клиент (покупатель):

- делает ежедневные закупки по каталогу, в котором представлены товары от нескольких поставщиков,
- в одном заказе можно указать товары от разных поставщиков,
- пользователь может авторизироваться, регистрироваться и восстанавливать пароль через API.
    
2. Поставщик:

- через API информирует сервис об обновлении прайса,
- может включать и отключать приём заказов,
- может получать список оформленных заказов (с товарами из его прайса).

**Базовая часть:**

Сервис под готовую спецификацию (API),
возможность добавления настраиваемых полей (характеристик) товаров,
импорт товаров,
отправка накладной на email администратора (для исполнения заказа),
отправка заказа на email клиента (подтверждение приёма заказа).

### Задача (взять за основу пример из репозитория, изучить его и выполнить продвинутую часть задания.)
За основу взят готовый пример. Произведены исправления и настройка проекта.  
Сформирован docker-compose файл для запуска приложения.  
Приложение протестировано с использованием запросов Postman.  
Доработка проекта. Версия = 1.0.0 22.02.2025:  
* экспорт товаров [100%] (выдача всего прайса магазина по запросу)✅, 
* админка заказов (проставление статуса заказа и уведомление клиента) [100%]✅,
* выделение медленных методов в отдельные асинхронные функции (email, импорт) [100%]✅,
* модификация админки django-baton [100%]✅

### Требования
- Python 3.10+
- Django
- Django Rest Framework
- Celery
- PostgreSQL
- Docker

### Документация
[Прочитайте документацию](https://github.com/Alonsole/Django_diplom/blob/main/Documentation.md)

### Лицензия
Это учебный проект вне коммерческих целей.

### Контакты
Проект не предполагает взаимодействий с пользователями.

   
