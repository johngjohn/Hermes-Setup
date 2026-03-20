#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILES=(/etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf)
READABLE=0

echo "[info] Reverse SSH is the default and recommended transport for this stack."
echo "[info] Goal: keep the reverse-forwarded listener bound to VPS loopback only."
echo "[info] Expected tunnel: ssh -N -R 127.0.0.1:${VPS_REMOTE_PORT}:127.0.0.1:${OBSIDIAN_LOCAL_PORT} -p ${VPS_SSH_PORT} ${VPS_USER}@${VPS_HOST}"

for file in "${CONFIG_FILES[@]}"; do
  if [ -r "$file" ]; then
    READABLE=1
    echo "[info] Inspecting $file"
    grep -Ei '^(AllowTcpForwarding|GatewayPorts|PermitOpen|Match)' "$file" || true
  fi
done

if [ "$READABLE" -eq 0 ]; then
  echo "[warn] sshd configuration files were not readable. Manually review sshd policy and runtime logs."
fi

echo "[info] Interpretation guidance:"
echo "- AllowTcpForwarding must allow reverse forwarding or Match rules must permit it for the tunnel user."
echo "- GatewayPorts does not need to expose the listener publicly because loopback-bound -R is the intended design."
echo "- If reverse forwarding is denied at runtime, check auth logs or journald for sshd messages."
