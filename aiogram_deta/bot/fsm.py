from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Literal

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    StorageKey,
    StateType,
    DEFAULT_DESTINY,
)
from deta import AsyncBase


class KeyBuilder(ABC):
    """
    Base class for Deta key builder
    """

    @abstractmethod
    def build(self, key: StorageKey, part: Literal["data", "state", "lock"]) -> str:
        """
        This method should be implemented in subclasses

        :param key: contextual key
        :param part: part of the record
        :return: key to be used in Redis queries
        """
        pass


class DefaultKeyBuilder(KeyBuilder):
    """
    Simple Deta key builder with default prefix.

    Generates a colon-joined string with prefix, chat_id, user_id,
    optional bot_id and optional destiny.
    """

    def __init__(
        self,
        *,
        prefix: str = "fsm",
        separator: str = ":",
        with_bot_id: bool = False,
        with_destiny: bool = False,
    ) -> None:
        """
        :param prefix: prefix for all records
        :param separator: separator
        :param with_bot_id: include Bot id in the key
        :param with_destiny: include destiny key
        """
        self.prefix = prefix
        self.separator = separator
        self.with_bot_id = with_bot_id
        self.with_destiny = with_destiny

    def build(self, key: StorageKey, part: Literal["data", "state", "lock"]) -> str:
        parts = [self.prefix]
        if self.with_bot_id:
            parts.append(str(key.bot_id))
        parts.extend([str(key.chat_id), str(key.user_id)])
        if self.with_destiny:
            parts.append(key.destiny)
        elif key.destiny != DEFAULT_DESTINY:
            raise ValueError(
                "Deta key builder is not configured to use key destiny other the default.\n"
                "\n"
                "Probably, you should set `with_destiny=True` in for DefaultKeyBuilder.\n"
                "E.g: `DetaStorage(deta_base, key_builder=DefaultKeyBuilder(with_destiny=True))`"
            )
        parts.append(part)
        return self.separator.join(parts)


class DetaFSMContext(BaseStorage):
    def __init__(
        self,
        deta_base: AsyncBase,
        key_builder: Optional[KeyBuilder] = None,
    ) -> None:
        if key_builder is None:
            key_builder = DefaultKeyBuilder()

        self.deta_base = deta_base
        self.key_builder = key_builder

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        record_key = self.key_builder.build(key, "state")
        state = state.state if isinstance(state, State) else state
        if state is None:
            await self.deta_base.delete(key=record_key)
        else:
            await self.deta_base.put({"state": state}, key=record_key)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        record_key = self.key_builder.build(key, "state")
        value = await self.deta_base.get(key=record_key)
        if not value:
            return None
        return value.get("state")

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        record_key = self.key_builder.build(key, "data")
        if not data:
            await self.deta_base.delete(key=record_key)
        else:
            await self.deta_base.put(data, key=record_key)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        record_key = self.key_builder.build(key, "data")
        result = await self.deta_base.get(key=record_key)
        if not result:
            return {}
        return result

    async def close(self) -> None:
        pass
