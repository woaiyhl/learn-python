#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[dev] 项目根目录: $ROOT_DIR"

if [ -f "$ROOT_DIR/mysql_demo/.env" ]; then
  echo "[dev] 读取 mysql_demo/.env 环境变量"
  # shellcheck disable=SC2046
  export $(grep -v '^#' "$ROOT_DIR/mysql_demo/.env" | xargs || true)
else
  echo "[dev] 警告: 未找到 mysql_demo/.env, 将使用代码中的默认 MySQL 配置"
fi

if command -v docker >/dev/null 2>&1 && command -v docker compose >/dev/null 2>&1; then
  echo "[dev] 使用 docker compose 启动 MySQL 容器 (服务名: mysql)"
  (cd "$ROOT_DIR" && docker compose up -d mysql)
  echo "[dev] MySQL 容器已启动，端口映射: ${MYSQL_PORT:-3306} -> 3306"
else
  echo "[dev] 未检测到 docker compose，将假定本机已有运行中的 MySQL 服务"
fi

echo "[dev] 启动 FastAPI 后端 (mysql_demo, 端口 8001)"
(
  cd "$ROOT_DIR" && \
  python -m uvicorn mysql_demo.main:app --reload --host 127.0.0.1 --port 8001
) &
BACKEND_PID=$!

echo "[dev] 启动 React 前端 (react_demo, 端口 5173)"
(
  cd "$ROOT_DIR/react_demo" && \
  npm run dev
) &
FRONTEND_PID=$!

cleanup() {
  echo "\n[dev] 收到退出信号, 正在停止服务..."
  if kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "[dev] 停止 FastAPI 后端 (PID=$BACKEND_PID)"
    kill "$BACKEND_PID" || true
  fi
  if kill -0 "$FRONTEND_PID" 2>/dev/null; then
    echo "[dev] 停止 React 前端 (PID=$FRONTEND_PID)"
    kill "$FRONTEND_PID" || true
  fi
  if command -v docker >/dev/null 2>&1 && command -v docker compose >/dev/null 2>&1; then
    echo "[dev] 你可以使用 'docker compose down' 手动停止 MySQL 容器 (当前脚本不自动关闭)"
  fi
}

trap cleanup INT TERM

echo "[dev] 所有服务已启动:"
echo "      后端: http://127.0.0.1:8001"
echo "      前端: http://localhost:5173"
echo "      API 文档: http://127.0.0.1:8001/docs"

wait

