from plugins.base import AbstractPlugin
from plugins import PLUGIN_NEW_CHAT_MEMBER


class MemberPlugin(AbstractPlugin):
    plugin_type = PLUGIN_NEW_CHAT_MEMBER


class RemoveMemberJoinedMessage(MemberPlugin):
    """Удаляет стандартное сообщение о новом участнике"""

    def execute(self, engine, message):
        try:
            if not hasattr(message, "new_chat_members") or not message.new_chat_members:
                return False  # Нечего обрабатывать

            for member in message.new_chat_members:
                chat_id = message.chat.id
                user_id = member.id

                try:
                    chat_member = engine._bot.get_chat_member(chat_id, user_id)
                except Exception as e:
                    self.log(f"Не удалось получить статус пользователя {user_id}: {e}", "error")
                    continue

                if chat_member.status in ["creator", "administrator"]:
                    self.log(f"Сообщение о вступлении админа/создателя {user_id} в чате {chat_id} пропущено")
                    return False

            # Если это не админ — удаляем сообщение
            engine.delete_message(message.chat.id, message.message_id)
            self.log(f"Удалено сообщение о новом участнике {user_id} в чате {chat_id}")
        except Exception as exc:
            self.log(f"Не удалось удалить сообщение {getattr(message, 'message_id', '?')}: {exc}", "error")

        return False
