from datetime import datetime, timedelta
from collections import defaultdict
import telebot
from plugins.base import AbstractPlugin, PLUGIN_NEW_CHAT_MESSAGE

class SpamRepeatPlugin(AbstractPlugin):
    plugin_type = PLUGIN_NEW_CHAT_MESSAGE

    def __init__(self, logger, engine, spam_threshold=1, mute_days=3, duplicate_window_hours=24):
        super().__init__(logger)
        self._engine = engine
        self._last_messages = defaultdict(lambda: defaultdict(list))
        self._warnings = defaultdict(lambda: defaultdict(lambda: {"count": 0, "last_warn": None}))
        self._spam_threshold = spam_threshold
        self._mute_duration = timedelta(days=mute_days)
        self._duplicate_window = timedelta(hours=duplicate_window_hours)
        self._warning_reset = timedelta(hours=24)  # сброс через 24 часа

    def escape_text(self, text: str) -> str:
        return ''.join(c for c in text if c.isalnum() or c.isspace())

    def execute(self, engine, message: telebot.types.Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        text = (message.text or "").strip().lower()
        now = datetime.utcnow()

        # Пропуск админов
        try:
            member = self._engine._bot.get_chat_member(chat_id, user_id)
            if member.status in ["creator", "administrator"]:
                self.log(f"Админ/владелец {user_id} отправил сообщение — спам не проверяем: {text}")
                return False
        except Exception as e:
            self.log(f"Не удалось получить статус пользователя {user_id}: {e}", "error")
            return False

        # Очистка старых сообщений
        user_messages = self._last_messages[chat_id][user_id]
        user_messages = [(msg_id, msg_text, ts) for (msg_id, msg_text, ts) in user_messages if now - ts < self._duplicate_window]
        self._last_messages[chat_id][user_id] = user_messages
        user_messages.append((message.message_id, text, now))

        # Поиск дубликатов
        duplicates = [msg_id for (msg_id, msg_text, _) in user_messages if msg_text == text]

        if len(duplicates) > self._spam_threshold:
            self.log(f"Обнаружен спам от {user_id} в чате {chat_id}: {text}")

            # Проверка предупреждений и сброс
            warn_data = self._warnings[chat_id][user_id]
            if warn_data["last_warn"] and now - warn_data["last_warn"] > self._warning_reset:
                warn_data["count"] = 0  # сброс после 24 часов

            warn_data["count"] += 1
            warn_data["last_warn"] = now
            self._warnings[chat_id][user_id] = warn_data

            clean_name = self.escape_text(message.from_user.full_name)
            if warn_data["count"] == 1:
                text_to_send = f"⚠️ Пользователь {clean_name}, это ваше первое предупреждение за спам. Следующее нарушение — мут на {self._mute_duration.days} дня."
            else:
                text_to_send = f"⚠️ Пользователь {clean_name}, вы уже предупреждались ({warn_data['count']-1}). За повторное нарушение — мут на {self._mute_duration.days} дня."

            try:
                self._engine.send_message(chat_id=chat_id, text=text_to_send)
                self.log(f"Отправлено предупреждение пользователю {user_id}, номер предупреждения: {warn_data['count']}")
            except Exception as e:
                self.log(f"Ошибка при отправке предупреждения {user_id}: {e}", "error")

            # Удаляем дубли
            for msg_id in duplicates[:-1]:
                try:
                    self._engine.delete_message(chat_id, msg_id)
                    self.log(f"Удалено повторное сообщение {msg_id} от пользователя {user_id}")
                except Exception as e:
                    self.log(f"Ошибка при удалении сообщения {msg_id}: {e}", "error")

            self._last_messages[chat_id][user_id] = [(duplicates[-1], text, now)]

            # Мутим пользователя
            try:
                duration_seconds = int(self._mute_duration.total_seconds())
                self._engine.mute_user(chat_id, user_id, duration_seconds)
                self.log(f"Пользователь {user_id} замучен на {self._mute_duration.days} дня за спам")
            except Exception as e:
                self.log(f"Ошибка при муте пользователя {user_id}: {e}", "error")

        return False
