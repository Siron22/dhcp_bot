# Используем базовый образ с поддержкой Python
FROM python:3.8

# Устанавливаем необходимые зависимости
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Запускаем бота
CMD ["python", "your_bot_script.py"]
