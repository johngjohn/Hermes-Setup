# Windows Local Setup

## Windows is the only optimized local platform

This repository is intentionally optimized for Windows 11 as the local machine and assumes home NAT is common.

## Steps

1. Install and open Obsidian Desktop.
2. Enable the Obsidian CLI REST or MCP-compatible plugin/service.
3. Record the local plugin port, usually `27124`.
4. Record the plugin API key.
5. Confirm `ssh.exe` exists, ideally at `C:\Windows\System32\OpenSSH\ssh.exe`.
6. Set `OBSIDIAN_API_KEY` and run `verify_windows_local.ps1` locally against `http://127.0.0.1:<local-port>/mcp`.
7. Run `setup_reverse_ssh_windows.ps1` to keep the reverse tunnel alive.

## Task Scheduler persistence notes

Recommended settings:

- Trigger: At log on for the Windows user that owns Obsidian.
- Action: Start `powershell.exe`.
- Arguments: `-ExecutionPolicy Bypass -File C:\path\to\setup_reverse_ssh_windows.ps1`.
- Enable automatic restart on failure.
- Use a Windows account that has access to the Obsidian environment.
