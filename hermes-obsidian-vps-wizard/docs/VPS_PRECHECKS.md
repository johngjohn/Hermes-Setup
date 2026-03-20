# VPS Prechecks

## Confirm OpenSSH server exists

```bash
sshd -T >/dev/null
```

## Check reverse forwarding support

```bash
bash ./sshd_reverse_forwarding_check.sh
```

Review `AllowTcpForwarding`, `GatewayPorts`, and any `Match` rules that may apply to the tunnel user.

## Check firewall posture

This design does not need the forwarded MCP port opened publicly because the remote listener should stay bound to localhost on the VPS.

## Test localhost binding

The Hermes MCP configuration should target `127.0.0.1:<remote-port>` only.

## Confirm curl availability

```bash
command -v curl
```
