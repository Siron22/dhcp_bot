from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from log_hadler2 import DhcpLogHandler  # Замените на фактический путь к вашему модулю

# Замените на ваш токен бота
TOKEN = '6320446687:AAFhS63Ab-5MTrGJU-fMZQJfXhXSjkVlEl0'

# Создаем экземпляр DhcpLogHandler
log_handler = DhcpLogHandler()


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для получения информации о подключенных устройствах.')


def connected_devices(update: Update, context: CallbackContext) -> None:
    devices = log_handler.connected_devices()

    if devices:
        response = [f"Устройств подключено: {len(devices)}"]
        response.extend([f"mac: {device['mac']}, ip: {device['ip']}" for device in devices])
    else:
        response = ["Нет подключенных устройств."]

    update.message.reply_text('\n'.join(response))


def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("connected_devices", connected_devices))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
