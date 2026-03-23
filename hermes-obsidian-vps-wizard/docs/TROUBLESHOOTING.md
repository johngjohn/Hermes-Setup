# Troubleshooting

## ssh.exe missing

- Install the Windows OpenSSH Client optional feature.
- Or point the script to `C:\Windows\System32\OpenSSH\ssh.exe`.
- Git for Windows `ssh.exe` can also work if you point to the full path.

## PowerShell execution policy

Run the generated scripts like this if the execution policy blocks them:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_reverse_ssh_windows.ps1
```

## Reverse forwarding denied

- Run `bash ./sshd_reverse_forwarding_check.sh` on the netcup VPS.
- Review `AllowTcpForwarding`, `GatewayPorts`, and `Match` blocks.
- Check sshd logs if the reverse tunnel is refused.

## netcup firewall or SCP networking confusion

- Confirm SSH to the netcup VPS still works normally.
- Review the SCP firewall if enabled.
- Remember that the reverse-forwarded MCP port is designed to stay private on `127.0.0.1`, so you normally should not open it publicly in the netcup firewall.

## Tunnel collapses after logout

- Keep the PowerShell loop alive in a persistent session.
- Use Task Scheduler to relaunch it at login or startup.

## Obsidian not open

If Obsidian is closed, the local plugin may not answer at all.

## Plugin not responding

- Re-enable the plugin in Obsidian.
- Confirm the plugin listens on the expected local port.
- Re-run `verify_windows_local.ps1`.

## Wrong key

A `401` or `403` usually means the Obsidian API key is wrong.

## Wrong port

- Check the Windows local port.
- Check the VPS remote forwarded port.
- Rebuild files if you changed one but not the others.

## Hermes not reading provider env

- Confirm the actual Hermes startup flow loads the intended env file.
- Verify `OPENAI_API_KEY` is present in the live environment Hermes sees.

## Hermes MCP config not merged

If Hermes starts but cannot reach Obsidian, the MCP snippet may not have been merged into the active Hermes config.

## OpenAI auth errors

- Re-check `OPENAI_API_KEY`.
- Restart Hermes after updating the env file.

## Model name typo

Only `gpt-5.4` and `gpt-5.4-mini` are accepted by this repository.

## Need emergency recovery on the VPS

If you break SSH or firewall settings, recover through the netcup SCP rescue system and then roll back the problematic changes.
