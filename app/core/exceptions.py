from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger


# 业务异常：在 service 层抛出，会被全局处理器捕获并返回统一格式
class BizException(Exception):
	def __init__(self, code: int = 400, msg: str = "error"):
		self.code = code
		self.msg = msg


# 统一错误码处理
def register_exception_handlers(app: FastAPI):
	@app.exception_handler(BizException)
	async def biz_exception_handler(request: Request, exc: BizException):
		return JSONResponse(
			status_code=exc.code,
			content={"code": exc.code, "msg": exc.msg, "data": None},
		)

	@app.exception_handler(HTTPException)
	async def http_exception_handler(request: Request, exc: HTTPException):
		return JSONResponse(
			status_code=exc.status_code,
			content={"code": exc.status_code, "msg": exc.detail, "data": None},
		)

	@app.exception_handler(RequestValidationError)
	async def validation_exception_handler(request: Request, exc: RequestValidationError):
		return JSONResponse(
			status_code=422,
			content={"code": 422, "msg": "Validation error", "data": exc.errors()},
		)

	@app.exception_handler(Exception)
	async def global_exception_handler(request: Request, exc: Exception):
		logger.exception("Unhandled exception")
		return JSONResponse(
			status_code=500,
			content={"code": 500, "msg": "Internal server error", "data": None},
		)
