# hermes-obsidian-vps-wizard

A Windows-first setup wizard repository for connecting a Linux VPS running Hermes Agent to an Obsidian Desktop instance on a local Windows 11 machine through a private reverse SSH tunnel, with OpenAI as the Hermes provider.

## 1. Purpose

This repository generates production-leaning scripts, config snippets, examples, and docs for this exact stack:

- Hermes Agent on a Linux VPS
- OpenAI API as Hermes' LLM provider
- Default model: `gpt-5.4`
- Optional cheaper/faster model: `gpt-5.4-mini`
- Obsidian Desktop on a local Windows 11 machine only
- Obsidian CLI REST or MCP-compatible local endpoint on that Windows machine only
- Hermes talking to Obsidian over MCP at `/mcp`
- Private reverse SSH tunnel from Windows to the VPS
- No public exposure by default
- No Obsidian Desktop or official Obsidian CLI on the VPS

## 2. Stack summary

- **Windows 11:** Obsidian Desktop, Obsidian REST/MCP plugin, API key, reverse SSH client loop
- **Linux VPS:** Hermes Agent, Hermes provider env file, Hermes MCP config, optional localhost healthcheck timer
- **Network path:** Windows `127.0.0.1:<local-port>` -> SSH reverse tunnel -> VPS `127.0.0.1:<remote-port>`
- **Secrets:** OpenAI key and Obsidian key are handled separately

## 3. ASCII architecture diagram

```text
[Windows 11 / Obsidian / Obsidian CLI REST]
  -> reverse SSH
  -> [VPS 127.0.0.1:37124]
  -> [Hermes MCP config points to localhost]
  -> [Hermes using OpenAI provider env]
```

## 4. What runs where

### Windows 11 only

- Obsidian Desktop
- Obsidian CLI REST or an MCP-compatible local plugin/service
- Obsidian API key
- `ssh.exe` reverse tunnel loop script
- Optional Task Scheduler persistence

### Linux VPS only

- Hermes Agent
- Hermes provider env file containing `OPENAI_API_KEY`
- Hermes MCP snippet pointing to `http://127.0.0.1:<remote-port>/mcp`
- Verification and sshd-precheck scripts
- Optional systemd healthcheck timer

## 5. Why this architecture is used

This design keeps the Obsidian vault and GUI local to the Windows 11 machine while giving a stable, remotely hosted Hermes Agent on the VPS access to the local Obsidian MCP endpoint through a private channel.

## 6. Why reverse SSH is preferred here

Reverse SSH is the default because the Windows machine is commonly behind home NAT, the reverse connection originates from the Windows side, and the forwarded listener can stay bound to `127.0.0.1` on the VPS.

## 7. Why Obsidian and the CLI are not on the VPS

The VPS should not host the Obsidian application, vault, or the official Obsidian CLI. This repository is intentionally built around a local-only Windows Obsidian runtime and a remote-only Hermes runtime.

## 8. Hermes OpenAI provider setup

Populate the generated provider env file with:

- `OPENAI_API_KEY=`
- `HERMES_MODEL=gpt-5.4`
- `OBSIDIAN_API_KEY=`
- `OBSIDIAN_LOCAL_PORT=27124`
- `VPS_HOST=`
- `VPS_SSH_PORT=22`
- `VPS_USER=`
- `VPS_REMOTE_PORT=37124`

The provider env file is separate from the Hermes MCP config snippet and separate from how you store the Windows-side Obsidian API key locally.

## 9. Model selection guidance

- Use `gpt-5.4` by default.
- Use `gpt-5.4-mini` when lower latency or lower cost matters more than maximum capability.
- The CLI enforces an allowlist of only these two model names.

## 10. Quickstart

```bash
python -m wizard.cli generate-example
python -m wizard.cli vps-setup
python -m wizard.cli windows-local-setup
python -m wizard.cli print-manual-steps
python -m wizard.cli verify
```

## 11. Ordered startup order

1. Prepare Obsidian Desktop and the local REST/MCP plugin on Windows.
2. Confirm the Windows-local `/mcp` endpoint works with the Obsidian API key.
3. Check VPS SSH reverse-forwarding support.
4. Install Hermes on the VPS.
5. Fill in the Hermes provider env file with the OpenAI key and model.
6. Merge the Hermes MCP snippet into the live Hermes config.
7. Start the Windows reverse SSH loop.
8. Verify the forwarded `/mcp` endpoint from the VPS.
9. Start Hermes and test the MCP integration.

## 12. Verification

- Run `powershell -ExecutionPolicy Bypass -File .\verify_windows_local.ps1 -LocalPort 27124 -ApiKey '<OBSIDIAN_API_KEY>'` on Windows.
- Run `bash ./sshd_reverse_forwarding_check.sh` on the VPS.
- Run `bash ./verify_vps_mcp.sh 37124 '<OBSIDIAN_API_KEY>'` on the VPS.
- Run `python -m wizard.cli verify` in this repository.

## 13. Changing ports

If you change the local Obsidian port or the VPS reverse-forwarded port, regenerate all relevant files and make sure the Windows reverse SSH script, Hermes provider env file, and Hermes MCP snippet all agree.

## 14. Rotating the OpenAI key

1. Update `OPENAI_API_KEY` in the real Hermes env file.
2. Restart Hermes or reload the environment used to launch it.
3. Leave the Obsidian key untouched unless it also changed.

## 15. Rotating the Obsidian key

1. Update the key where it is stored locally on Windows.
2. Update the key used for VPS verification.
3. Update any Hermes env file copy of `OBSIDIAN_API_KEY` if you store it there.
4. Re-run both verification scripts.

## 16. Common mistakes

- Installing Obsidian or the official Obsidian CLI on the VPS
- Forgetting to merge `hermes_mcp_snippet.yaml` into the live Hermes config
- Using an unsupported model name
- Exposing the reverse-forwarded port publicly instead of loopback-only
- Testing from the VPS before the Windows reverse tunnel is running
- Mixing up the OpenAI and Obsidian API keys
- Forgetting that the Windows side is usually behind home NAT

## 17. File overview

- `wizard/` — Python CLI, models, validation, rendering, and checks
- `templates/` — source templates for generated files
- `generated_examples/` — checked-in example outputs using dummy values
- `docs/` — manual setup, troubleshooting, security, Windows setup, and VPS prechecks
- `.env.example` — Windows-local example values for the reverse SSH loop

## Repository commands

```bash
python -m wizard.cli vps-setup
python -m wizard.cli windows-local-setup
python -m wizard.cli verify
python -m wizard.cli print-manual-steps
python -m wizard.cli generate-example
python -m wizard.cli dry-run-all
```
