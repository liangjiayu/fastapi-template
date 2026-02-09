from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PageData(BaseModel, Generic[T]):
	list: list[T]
	total: int
	page: int
	page_size: int


class ApiResponse(BaseModel, Generic[T]):
	code: int = 200
	msg: str = "success"
	data: T | None = None

	@staticmethod
	def ok(data: Any = None, msg: str = "success") -> dict:
		return {"code": 200, "msg": msg, "data": data}

	@staticmethod
	def fail(code: int = 400, msg: str = "error") -> dict:
		return {"code": code, "msg": msg, "data": None}

	@staticmethod
	def page(list: list, total: int, page: int, page_size: int) -> dict:
		return {
			"code": 200,
			"msg": "success",
			"data": {"list": list, "total": total, "page": page, "page_size": page_size},
		}
