# bot_buttons.py

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import plugins
from plugins.spam_repeat_plugin import SpamRepeatPlugin

# --- Меню админа в киберпанк стиле ---
def get_admin_menu():
    keyboard = [
        [InlineKeyboardButton("╔══ АНТИСПАМ ══╗", callback_data="toggle_spam")],
        # Кнопку авто-бан убрали, т.к. CASBan нет
        [InlineKeyboardButton("╔══ ПОМОЩЬ / FAQ ══╗", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Отправка меню админу ---
def send_admin_menu(bot, chat_id):
    bot.send_message(chat_id, "┌─── МЕНЮ ЗАЩИТЫ ───┐", reply_markup=get_admin_menu())

# --- Обработчик нажатий на кнопки ---
def handle_admin_callback(bot, call, engine):
    data = call.data
    if data == "toggle_spam":
        # Поиск плагина SpamRepeatPlugin
        plugin = next(
            (p for p in engine._plugins[plugins.PLUGIN_NEW_CHAT_MESSAGE]
             if isinstance(p, SpamRepeatPlugin)), None
        )
        if plugin:
            plugin.enabled = not getattr(plugin, "enabled", True)
            status = "ВКЛ" if plugin.enabled else "ВЫКЛ"
            bot.answer_callback_query(call.id, f"╔══ АНТИСПАМ {status} ══╗")
    elif data == "help":
        bot.answer_callback_query(
            call.id,
            "╔══ ПОМОЩЬ ══╗\nБот защищает чат от спама и повторов сообщений.\nИспользуйте кнопки для управления защитой."
        )
