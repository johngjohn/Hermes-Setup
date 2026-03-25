# Day-2 Ops Runbook (Operator-first)

This runbook is for ongoing operation after initial setup.

## Daily quick checks

1. Confirm gateway service is up on VPS.
2. Confirm reverse SSH loop is running on Windows.
3. Confirm MCP endpoint responds through VPS localhost.
4. Confirm Hermes can complete a simple Obsidian read action.
5. Confirm `hermes_model_routing.yaml` still matches your preferred routing strategy.

## Commands

### VPS checks

```bash
# Gateway status (example service)
systemctl --user status hermes-gateway.service --no-pager

# Wizard artifact integrity
cd hermes-obsidian-vps-wizard
python -m wizard.cli verify

# Tunnel + MCP check (prompts for Obsidian key)
bash ./verify_vps_mcp.sh 37124
```

### Windows checks

```powershell
# Local plugin check
powershell -ExecutionPolicy Bypass -Command "$env:OBSIDIAN_API_KEY='<OBSID...KEY>'; .\verify_windows_local.ps1 -LocalPort 27124"

# Tunnel loop
powershell -ExecutionPolicy Bypass -File .\setup_reverse_ssh_windows.ps1
```

## Recovery sequence

If Hermes cannot reach Obsidian:

1. Verify Obsidian app/plugin is running on Windows.
2. Run `verify_windows_local.ps1` and fix local errors first.
3. Re-establish reverse SSH loop on Windows.
4. Run `sshd_reverse_forwarding_check.sh` on VPS.
5. Run `verify_vps_mcp.sh` on VPS.
6. Restart Hermes gateway on VPS.

## Key rotation

### OpenAI key (VPS)

1. Update `OPENAI_API_KEY` in VPS env file.
2. Restart Hermes process.
3. Verify normal model calls.

### Obsidian key (Windows-only)

1. Rotate in Windows plugin config.
2. Re-run Windows local verification.
3. Re-run VPS verification and enter new key interactively.
4. Do not store key persistently on VPS.

## Change discipline

- Make one change at a time.
- Re-run `python -m wizard.cli verify` after edits.
- Commit generated outputs with template/code changes in the same PR.
