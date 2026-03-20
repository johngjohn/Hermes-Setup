#!/usr/bin/env bash
set -euo pipefail

REMOTE_PORT="${1:-37124}"
API_KEY="${2:-}"
URL="http://127.0.0.1:${REMOTE_PORT}/mcp"
TMP_BODY="$(mktemp)"
trap 'rm -f "$TMP_BODY"' EXIT

if ! command -v curl >/dev/null 2>&1; then
  echo "[error] curl is required on the VPS." >&2
  exit 1
fi

if [ -z "$API_KEY" ]; then
  echo "Usage: $0 <remote-port> <obsidian-api-key>"
  exit 2
fi

echo "[info] Checking VPS-local MCP endpoint at $URL"
HTTP_CODE="$(curl -sS -o "$TMP_BODY" -w '%{http_code}' \
  -H "Authorization: Bearer ${API_KEY}" \
  --connect-timeout 10 \
  --max-time 20 \
  "$URL" || true)"

echo "[info] HTTP status: ${HTTP_CODE}"
case "$HTTP_CODE" in
  200|204)
    echo "[ok] MCP endpoint answered successfully through the reverse tunnel."
    ;;
  401|403)
    echo "[warn] Unauthorized. The tunnel is likely up, but the Obsidian API key is wrong."
    ;;
  000)
    echo "[warn] No response. Likely causes: tunnel down, Obsidian closed, plugin disabled, timeout, or sshd reverse forwarding denied."
    ;;
  *)
    echo "[warn] Unexpected HTTP status. Review tunnel state, API key, plugin health, and sshd policy."
    ;;
esac
