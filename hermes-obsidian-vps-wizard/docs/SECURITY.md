# Security

## Separate handling of OpenAI and Obsidian secrets

Treat `OPENAI_API_KEY` and `OBSIDIAN_API_KEY` as different credentials with different blast radii. Rotate them separately and store them separately when possible.

## Loopback-only forwarding

The recommended SSH command binds the forwarded VPS listener to `127.0.0.1` only. That keeps the MCP endpoint private to the VPS.

## Windows local threat surface

The local Obsidian plugin is still a local attack surface on the Windows machine. Keep it bound to loopback and protect the Windows session.

## SSH key authentication recommendation

Prefer SSH key authentication for the Windows-to-VPS tunnel instead of passwords.

## Public exposure risks

Avoid `GatewayPorts yes` style public exposure for this workflow. The design target is a private loopback-only listener on the VPS.

## Least privilege

Use a dedicated VPS user for the reverse tunnel and Hermes if practical.

## Rotate both credentials

- Rotate the OpenAI key if your LLM credential leaks.
- Rotate the Obsidian key if local plugin credentials leak.
- Re-run verification after either rotation.

## Store env files safely

- Keep real env files out of git.
- Use restrictive permissions on VPS env files.
- Store Windows-side copies where only the intended Windows user can access them.
