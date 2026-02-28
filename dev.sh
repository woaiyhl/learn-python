#!/usr/bin/env bash
set -euo pipefail
set -m

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BACKEND="${BACKEND:-mysql_demo}"
FRONTEND="${FRONTEND:-react_demo}"

BACKEND_HOST="${BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${BACKEND_PORT:-8001}"
FRONTEND_HOST="${FRONTEND_HOST:-127.0.0.1}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

USE_SQLITE="${USE_SQLITE:-1}"

backend_dir="${ROOT_DIR}/${BACKEND}"
frontend_cwd="${ROOT_DIR}/${FRONTEND}"

if [[ ! -d "${backend_dir}" ]]; then
  echo "后端目录不存在: ${backend_dir}"
  exit 1
fi

if [[ ! -d "${frontend_cwd}" ]]; then
  echo "前端目录不存在: ${frontend_cwd}"
  exit 1
fi

cleanup() {
  if [[ -n "${FRONT_PID:-}" ]]; then
    kill -TERM -- "-${FRONT_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${BACK_PID:-}" ]]; then
    kill -TERM -- "-${BACK_PID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT INT TERM

echo "启动后端: ${BACKEND} (${BACKEND_HOST}:${BACKEND_PORT})"
(
  cd "${ROOT_DIR}"
  if [[ "${BACKEND}" == "mysql_demo" ]]; then
    USE_SQLITE="${USE_SQLITE}" python3 -m uvicorn mysql_demo.main:app --reload --host "${BACKEND_HOST}" --port "${BACKEND_PORT}"
  elif [[ "${BACKEND}" == "advanced_demo" ]]; then
    python3 -m uvicorn advanced_demo.main:app --reload --host "${BACKEND_HOST}" --port "${BACKEND_PORT}"
  else
    echo "不支持的后端: ${BACKEND}"
    exit 1
  fi
) &
BACK_PID=$!

backend_probe_path="/health"
if [[ "${BACKEND}" == "advanced_demo" ]]; then
  backend_probe_path="/docs"
fi

echo "等待后端就绪: http://${BACKEND_HOST}:${BACKEND_PORT}${backend_probe_path}"
for _ in {1..60}; do
  if python3 -c "import urllib.request; urllib.request.urlopen('http://${BACKEND_HOST}:${BACKEND_PORT}${backend_probe_path}', timeout=0.5).read()" >/dev/null 2>&1; then
    echo "后端已就绪"
    break
  fi
  sleep 0.25
done

echo "启动前端: ${FRONTEND} (${FRONTEND_HOST}:${FRONTEND_PORT})"
(
  cd "${frontend_cwd}"
  npm run dev -- --host "${FRONTEND_HOST}" --port "${FRONTEND_PORT}"
) &
FRONT_PID=$!

echo "前端地址: http://${FRONTEND_HOST}:${FRONTEND_PORT}/"
echo "按 Ctrl+C 退出"

wait
