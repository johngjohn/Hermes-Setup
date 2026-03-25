[Unit]
Description=Hermes Obsidian MCP localhost healthcheck
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=%h/hermes-obsidian-vps-wizard
ExecStart=/usr/bin/env bash %h/hermes-obsidian-vps-wizard/verify_vps_mcp.sh ${VPS_REMOTE_PORT}
