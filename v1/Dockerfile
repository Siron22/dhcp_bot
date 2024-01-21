# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем зависимости
RUN pip install --no-cache-dir python-telegram-bot

# Копируем ваш код в контейнер
COPY . /app

# Рабочая директория
WORKDIR /app

# Запускаем ваш бот
CMD ["python", "main.py"]