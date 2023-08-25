from datetime import datetime
from typing import Union, List, Any
from dataclasses import dataclass

from deta.base import FetchResponse

from deta import AsyncBase


@dataclass
class GetResponse:
    key: str
    data: Union[str, dict]

    def __getattr__(self, item):
        try:
            return self.data[item]
        except KeyError:
            raise AttributeError(
                f"The <{item}> attribute is not in the key data."
            )

    def get(self, key: str = "value", default: [Any, None] = None):
        return self.data.get(key, default)


class DetaBase:
    def __init__(
        self,
        deta_base: AsyncBase,
    ) -> None:
        self.deta_base = deta_base

    async def close(self) -> None:
        await self.deta_base.close()

    async def get(self, key: str) -> Union[GetResponse, None]:
        if result := await self.deta_base.get(key=key):
            return GetResponse(
                result.pop('key'),
                result,
            )

    async def delete(self, key: str) -> None:
        return await self.deta_base.delete(key=key)

    async def insert(
        self,
        data: Union[dict, list, str, int, bool],
        key: str = None,
        *,
        expire_in: int = None,
        expire_at: Union[int, float, datetime] = None,
    ):
        return await self.deta_base.insert(
            data=data,
            key=key,
            expire_in=expire_in,
            expire_at=expire_at,
        )

    async def put(
        self,
        data: Union[dict, list, str, int, bool],
        key: str = None,
        *,
        expire_in: int = None,
        expire_at: Union[int, float, datetime] = None,
    ):
        return await self.deta_base.put(
            data=data,
            key=key,
            expire_in=expire_in,
            expire_at=expire_at,
        )

    async def put_many(
        self,
        items: List[Union[dict, list, str, int, bool]],
        *,
        expire_in: int = None,
        expire_at: Union[int, float, datetime] = None,
    ):
        return await self.deta_base.put_many(
            items=items,
            expire_in=expire_in,
            expire_at=expire_at,
        )

    async def fetch(
        self,
        query: Union[dict, list] = None,
        *,
        limit: int = 1000,
        last: str = None,
        desc: bool = False,
    ) -> FetchResponse:
        return await self.deta_base.fetch(
            query=query,
            limit=limit,
            last=last,
            desc=desc,
        )

    async def update(
        self,
        updates: dict,
        key: str,
        *,
        expire_in: int = None,
        expire_at: Union[int, float, datetime] = None,
    ) -> None:
        return await self.deta_base.update(
            updates=updates,
            key=key,
            expire_in=expire_in,
            expire_at=expire_at,
        )
