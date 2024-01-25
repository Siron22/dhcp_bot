# Используем базовый образ с поддержкой Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем необходимые зависимости
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота в контейнер
COPY . /app

# Запускаем бота
CMD ["python3", "main.py"]
