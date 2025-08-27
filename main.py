import os
import signal
import sys

import telebot
from dotenv import load_dotenv

from bot import Engine
from logger import Logger
from plugins.members import RemoveMemberJoinedMessage
from plugins.chat_message import TestPlugin
from plugins.spam_repeat_plugin import SpamRepeatPlugin
from storage import FileSystem
from metrics import start_metrics_server, BotMetrics

def main():
    load_dotenv()
    start_metrics_server(int(os.getenv("METRICS_PORT", "9090")), os.getenv("METRICS_HOST", "127.0.0.1"))

    bot_metrics = BotMetrics()
    storage = FileSystem(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "storage"))
    bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
    logger = Logger("BOT")
    engine = Engine(os.getenv("TELEGRAM_BOT_USERNAME"), bot, bot_metrics, storage, logger)

    # Подключаем плагины
    engine.add_plugin(RemoveMemberJoinedMessage(Logger("RemoveMemberJoinedMessage")))
    engine.add_plugin(TestPlugin(Logger("TestPlugin")))
    engine.add_plugin(SpamRepeatPlugin(Logger("SpamRepeatPlugin"), engine))

    @bot.message_handler(commands=["unmute"])
    def unmute_command(message: telebot.types.Message):
        args = message.text.split()
        if len(args) != 2 or not args[1].isdigit():
            bot.reply_to(message, "Использование: /unmute <user_id>")
            return
        user_id = int(args[1])
        try:
            engine.unban_user(message.chat.id, user_id)
            bot.reply_to(message, f"Пользователь {user_id} разблокирован.")
            logger.info(f"Admin {message.from_user.id} unmuted user {user_id}")
        except Exception as e:
            bot.reply_to(message, f"Ошибка при разблокировке: {e}")
            logger.error(f"Ошибка при разблокировке {user_id}: {e}")

    def handle_ctrlc(signum, frame):
        print("\n*** Ctrl-C pressed. Stopping bot... ")
        engine.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_ctrlc)
    signal.signal(signal.SIGTERM, handle_ctrlc)

    engine.start()

if __name__ == "__main__":
    main()
