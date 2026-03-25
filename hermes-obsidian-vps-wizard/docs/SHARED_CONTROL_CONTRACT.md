# Shared Control Contract (John + Ariel/Hermes)

This document defines how control is shared between John (human operator) and Ariel/Hermes (agent running on VPS).

## Purpose

- Keep day-to-day vault operations fast.
- Keep security boundaries explicit.
- Prevent accidental destructive changes.

## Control boundaries

### Ariel/Hermes can do autonomously

- Read/search the vault through MCP tools.
- Propose note edits and generate content drafts.
- Execute routine verification and health checks on VPS side.
- Open PRs and update this repository when requested.

### Ariel/Hermes should request confirmation first

- Bulk note rewrites or folder-wide refactors.
- Any deletion, rename, or move that affects many notes.
- Any change that alters long-lived policy/security defaults.
- Any operation that could expose services publicly.

## Key handling rules

- `OPENAI_API_KEY` may exist on VPS in Hermes provider env.
- `OBSIDIAN_API_KEY` is Windows-local only.
- Do not persist `OBSIDIAN_API_KEY` in VPS env files.
- VPS verification may prompt for the Obsidian key interactively when needed.

## Operational expectations

- Prefer small, reversible changes.
- Keep command examples copy-paste ready.
- Keep generated outputs and templates in sync.
- Record major workflow changes in this repository before relying on them.

## Incident rule

If behavior is unexpected or unsafe, stop automation and fall back to manual operator confirmation before continuing.
