#!/usr/bin/env bash
set -euo pipefail

HERMES_DIR="$HOME/.hermes"
CONFIG_PATH="${HERMES_CONFIG_PATH}"
ENV_PATH="${HERMES_ENV_PATH}"
BACKUP_SUFFIX="$(date +%Y%m%d%H%M%S)"

mkdir -p "$HERMES_DIR"
chmod 700 "$HERMES_DIR"

echo "[info] Hermes directory ensured at $HERMES_DIR"
echo "[info] This script assumes a netcup vServer / VPS running Linux."
echo "[info] OpenAI provider environment file belongs at: $ENV_PATH"
echo "[info] Merge hermes_mcp_snippet.yaml into: $CONFIG_PATH"
echo "[info] Default model for this stack: ${HERMES_MODEL}"
echo "[info] Obsidian Desktop and the Obsidian CLI REST service must stay on the Windows 11 machine, not on the netcup VPS."
echo "[info] Before troubleshooting network issues, review SSH reachability and the netcup SCP firewall posture."

if [ -f "$CONFIG_PATH" ]; then
  cp "$CONFIG_PATH" "$CONFIG_PATH.$BACKUP_SUFFIX.bak"
  echo "[info] Existing Hermes config backed up to $CONFIG_PATH.$BACKUP_SUFFIX.bak"
else
  install -m 600 /dev/null "$CONFIG_PATH"
  echo "[info] Created placeholder Hermes config at $CONFIG_PATH"
fi

if [ ! -f "$ENV_PATH" ]; then
  install -m 600 /dev/null "$ENV_PATH"
  echo "[info] Created placeholder provider env file at $ENV_PATH"
else
  chmod 600 "$ENV_PATH"
  echo "[info] Existing provider env file permissions normalized to 600"
fi

cat <<MSG
Next steps:
1. Copy hermes_provider_env.example into $ENV_PATH and add OPENAI_API_KEY and OBSIDIAN_API_KEY.
2. Merge hermes_mcp_snippet.yaml into $CONFIG_PATH without deleting unrelated Hermes settings.
3. Run ./sshd_reverse_forwarding_check.sh to confirm sshd allows reverse forwarding on the netcup VPS.
4. Confirm the netcup SCP firewall does not interfere with SSH management access.
5. Bring up the Windows reverse SSH loop.
6. Run ./verify_vps_mcp.sh ${VPS_REMOTE_PORT} '<OBSIDIAN_API_KEY>' once the tunnel is active.
MSG
