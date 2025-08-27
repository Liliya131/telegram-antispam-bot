from __future__ import annotations
from abc import ABC, abstractmethod
import telebot
import bot
from logger import Logger

PLUGIN_NEW_CHAT_MESSAGE = 1
PLUGIN_NEW_CHAT_MEMBER = 2


class AbstractPlugin(ABC):
    """Base class for all plugins."""

    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    @abstractmethod
    def execute(self, engine: bot.Engine, message: telebot.types.Message) -> bool | None:
        """
        Выполняет логику плагина.
        Возвращает:
          - True  → сообщение обработано, прерываем дальнейшие плагины
          - False → передаём сообщение дальше
          - None  → плагин ничего не сделал
        """
        pass

    def log(self, msg: str, severity: str = "info") -> None:
        """Логирование с поддержкой разных уровней"""
        log_msg = f"[{self.__class__.__name__}] {msg}"
        match severity:
            case "debug":
                getattr(self._logger, "debug", self._logger.info)(log_msg)
            case "warning":
                getattr(self._logger, "warning", self._logger.info)(log_msg)
            case "error":
                getattr(self._logger, "error", self._logger.info)(log_msg)
            case "critical":
                getattr(self._logger, "critical", self._logger.info)(log_msg)
            case _:
                self._logger.info(log_msg)
