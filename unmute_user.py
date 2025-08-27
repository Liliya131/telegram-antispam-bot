import os
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

chat_id = -1002960727643
user_id = 5404627260

bot.restrict_chat_member(
    chat_id=chat_id,
    user_id=user_id,
    permissions=telebot.types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=False,
        can_invite_users=True,
        can_pin_messages=False
    )
)

print(f"Пользователь {user_id} разблокирован в чате {chat_id}.")
