from abc import ABC, abstractmethod

from fastapi import FastAPI


class StartUpProviderMixin(ABC):
    """
    Миксин для обработки FastAPI startup event.

    Атрибуты:
        - app (FastAPI): Экземпляр FastAPI.

    Методы:
        - startup: Абстрактный метод для обработки события startup.
        - _register_startup_event: Регистрация события startup.
        - register_events: Регистрация всех событий.
    """

    app: FastAPI

    @abstractmethod
    async def startup(self) -> None:
        """FastAPI startup event"""
        raise NotImplementedError

    def _register_startup_event(self) -> None:
        self.app.add_event_handler("startup", self.startup)

    def register_events(self) -> None:
        self._register_startup_event()


class ShutDownProviderMixin(ABC):
    """
    Миксин для обработки FastAPI события shutdown.

    Атрибуты:
        - app (FastAPI): Экземпляр FastAPI.

    Методы:
        - shutdown: Абстрактный метод для обработки события shutdown.
        - _register_shutdown_event: Регистрация события shutdown.
        - register_events: Регистрация всех событий.
    """

    app: FastAPI

    @abstractmethod
    async def shutdown(self) -> None:
        """FastAPI shutdown event"""
        raise NotImplementedError

    def _register_shutdown_event(self) -> None:
        self.app.add_event_handler("shutdown", self.shutdown)

    def register_events(self) -> None:
        self._register_shutdown_event()


class BaseProvider(StartUpProviderMixin, ShutDownProviderMixin):
    """
    Базовый провайдер, включающий в себя обработку обоих событий: startup и shutdown.

    Методы:
        - register_events: Регистрация всех событий.
    """

    def register_events(self) -> None:
        self._register_startup_event()
        self._register_shutdown_event()
