# ---- 构建阶段 ----
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

# 预编译字节码加速启动 | 复制模式避免硬链接问题 | 不安装开发依赖
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1

WORKDIR /app

# 先只复制依赖清单，利用 Docker 层缓存
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project

# 再复制源码，完成项目安装
COPY . .
RUN uv sync

# ---- 运行阶段 ----
FROM python:3.14-slim-bookworm

# 创建非 root 用户
RUN groupadd --system appuser && \
    useradd --system --gid appuser appuser

# 从构建阶段复制应用（含 .venv 和源码）
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

USER appuser

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
