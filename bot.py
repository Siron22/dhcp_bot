from dotenv import load_dotenv, find_dotenv
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from log_handler import DhcpLogHandler

# Load all environment variables
load_dotenv(find_dotenv())

# Initialize log handler
dhcp_handler = DhcpLogHandler()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")
CHAT_ID = getenv("CHAT_ID")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    welcome_message = "This bot provides information about connected devices..\n" \
                      "Use the /devices command to get a list of connected devices.\n" \
                      "Use the /update to receive updated info.\n" \
                      "Use the /log to receive info about all DHCPACK requests."
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n"
                         f"{welcome_message}")


@dp.message(Command('devices'))
async def show_devices(message: types.Message):
    devices_info = "\n".join(
        [f"{device['date_time']} MAC: {device['mac']}, IP: {device['ip']}" for device in
         dhcp_handler.get_approved_devices])
    response = f"Approved devices:\n{devices_info}"
    await message.answer(response)


@dp.message(Command('update'))
async def update_connections(message: types.Message):
    new_device = dhcp_handler.monitor_dhcp_log()
    response = str()
    if new_device:
        for device in new_device:
            status = "new device" if dhcp_handler.new else "previous device"
            response = (f"{device['date_time']} New DHCPACK for {device['mac']}. \nAddress: {device['ip']}\n"
                        f"Status: {status}")
            dhcp_handler.clear_new()
    else:
        response = f"No new DHCPACK requests"
    await message.answer(response)


@dp.message(Command('log'))
async def show_devices(message: types.Message):
    first = dhcp_handler.get_ack_requests[0]["date_time"]
    last = dhcp_handler.get_ack_requests[-1]["date_time"]
    quantity = len(dhcp_handler.get_ack_requests)
    response = f"{quantity} DHCPACK responses from {first} to {last}"
    await message.answer(response)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)
    # And the run events dispatching
    await dp.start_polling(bot)
