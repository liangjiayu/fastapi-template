import builtins
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageData(BaseModel, Generic[T]):
	list: builtins.list[T] = Field(description="数据列表")
	total: int = Field(description="总记录数")
	page: int = Field(description="当前页码")
	page_size: int = Field(description="每页条数")


class ApiResponse(BaseModel, Generic[T]):
	code: int = Field(200, description="业务状态码")
	msg: str = Field("success", description="提示信息")
	data: T | None = Field(None, description="响应数据")

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
