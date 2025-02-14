# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Явно устанавливаем gunicorn
RUN pip install gunicorn

# Копируем остальные файлы проекта в контейнер
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Запускаем команду для запуска сервера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "netology_pd_diplom.wsgi"]