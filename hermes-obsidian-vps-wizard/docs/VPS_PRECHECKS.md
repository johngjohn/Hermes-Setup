# VPS Prechecks for netcup vServer / VPS

## Confirm the server is provisioned in SCP

In the netcup **Server Control Panel (SCP)**, confirm the VPS is online, has the expected image installed, and has the correct public IPv4 and/or IPv6 assigned.

## Confirm OpenSSH server exists

```bash
sshd -T >/dev/null
```

## Check reverse forwarding support

```bash
bash ./sshd_reverse_forwarding_check.sh
```

Review `AllowTcpForwarding`, `GatewayPorts`, and any `Match` rules that may apply to the tunnel user.

## Check the netcup SCP firewall posture

If you use the netcup firewall, make sure it is not blocking SSH access to the VPS. The forwarded MCP port does **not** need to be opened publicly when you keep the reverse listener bound to localhost.

## Test localhost binding

The Hermes MCP configuration should target `127.0.0.1:<remote-port>` only.

## Confirm curl availability

```bash
command -v curl
```

## Rescue system fallback

If you lock yourself out or break the SSH configuration, netcup provides a rescue system through SCP. Use it to recover SSH access or revert configuration mistakes.
