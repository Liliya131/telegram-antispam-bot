import telebot
from plugins.base import AbstractPlugin
from plugins import PLUGIN_NEW_CHAT_MESSAGE


class ChatMessagePlugin(AbstractPlugin):
    plugin_type = PLUGIN_NEW_CHAT_MESSAGE


class TestPlugin(ChatMessagePlugin):
    """Тестовый плагин для безопасного логирования сообщений"""

    def execute(self, engine, message: telebot.types.Message):
        # Подстраховка от отсутствующих данных
        if not hasattr(message, "from_user") or not hasattr(message, "chat"):
            self.log("Получено сообщение без from_user или chat — пропускаем", "warning")
            return False

        user_id = message.from_user.id
        user_name = message.from_user.full_name
        chat_id = message.chat.id
        text = message.text or ""
        content_type = getattr(message, "content_type", "unknown")

        try:
            member = engine._bot.get_chat_member(chat_id, user_id)
            if member.status in ["creator", "administrator"]:
                self.log(
                    f"Админ/владелец {user_name} ({user_id}) "
                    f"в чате {chat_id} отправил {content_type}: {text}"
                )
                return False
        except Exception as e:
            self.log(f"Не удалось получить статус пользователя {user_id}: {e}", "error")
            return False

        self.log(
            f"Пользователь {user_name} ({user_id}) "
            f"в чате {chat_id} отправил {content_type}: {text}"
        )
        return False
