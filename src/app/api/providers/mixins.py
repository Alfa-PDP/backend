from abc import ABC, abstractmethod

from fastapi import FastAPI


class StartUpProviderMixin(ABC):
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
    def register_events(self) -> None:
        self._register_startup_event()
        self._register_shutdown_event()
