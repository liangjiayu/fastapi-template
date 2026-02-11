import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
	"""配置 Loguru 日志系统

	- 控制台输出：彩色格式化，便于开发调试
	- 文件输出：按天轮转，保留 7 天，用于生产环境追踪
	"""
	# 移除默认的 handler
	logger.remove()

	# 控制台输出配置
	log_format = (
		"<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
		"<level>{level: <8}</level> | "
		"<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
		"<level>{message}</level>"
	)

	logger.add(
		sys.stdout,
		format=log_format,
		level=settings.LOG_LEVEL,
		colorize=True,
	)

	# 文件输出配置（可选）
	if settings.LOG_FILE_ENABLED:
		log_dir = Path("logs")
		log_dir.mkdir(exist_ok=True)

		logger.add(
			log_dir / "app.log",
			format=log_format,
			level=settings.LOG_LEVEL,
			rotation=settings.LOG_FILE_ROTATION,
			retention=settings.LOG_FILE_RETENTION,
			compression="zip",  # 压缩旧日志节省空间
			encoding="utf-8",
		)

	logger.info(f"Logging configured: level={settings.LOG_LEVEL}, file_enabled={settings.LOG_FILE_ENABLED}")
