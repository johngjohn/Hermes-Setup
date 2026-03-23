# Manual Setup

This document prints the exact ordered manual process that the wizard automates for a **netcup vServer / VPS**.

## Ordered manual steps

1. In the netcup **Server Control Panel (SCP)**, install a Linux image on the VPS, typically Debian or Ubuntu.
2. Confirm SSH access to the netcup VPS and finish your base hardening.
3. On Windows 11, open Obsidian Desktop with the vault Hermes should use.
4. Enable the Obsidian CLI REST or MCP-compatible plugin/service inside Obsidian.
5. Extract the plugin API key and store it locally on Windows.
6. Confirm the plugin is listening on `127.0.0.1:27124` or your chosen local port.
7. Run `verify_windows_local.ps1` with the Obsidian API key and confirm the local `/mcp` endpoint answers.
8. On the netcup VPS, confirm the OpenSSH server is installed and running.
9. Run `sshd_reverse_forwarding_check.sh` and review `AllowTcpForwarding`, `GatewayPorts`, `Match` rules, and the netcup SCP firewall posture.
10. Install Hermes on the netcup VPS and create or update the provider env file containing the OpenAI API key.
11. Merge `hermes_mcp_snippet.yaml` into `~/.hermes/config.yaml` so Hermes points at `http://127.0.0.1:<remote-port>/mcp`.
12. Start `setup_reverse_ssh_windows.ps1` so Windows opens the reverse SSH tunnel to the netcup VPS.
13. Run `verify_vps_mcp.sh` on the netcup VPS and confirm the forwarded endpoint responds.
14. Start Hermes and perform an end-to-end Obsidian MCP test.
