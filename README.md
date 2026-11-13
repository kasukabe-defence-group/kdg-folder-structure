# KDG server context

A **context-only map** of the KDG Cloud server for prompting an LLM. This is not application source, a backup, a runnable deployment, or an exact live filesystem inventory.

## Give an LLM these files

1. [LLM_CONTEXT.md](LLM_CONTEXT.md) — architecture, workflows, constraints, and unresolved issues.
2. [SERVER_TREE.md](SERVER_TREE.md) — readable directory tree and container mounts.
3. [docs/MINECRAFT_SERVER_GUIDE.md](docs/MINECRAFT_SERVER_GUIDE.md) — creation options explained.
4. [AGENTS.md](AGENTS.md) — guidance for coding agents using this repository.

Example prompt:

> Read LLM_CONTEXT.md, SERVER_TREE.md, and AGENTS.md from https://github.com/kasukabe-defence-group/kdg-folder-structure. Treat server/ as descriptive placeholders, not source code. My task is: [describe the task]. Ask for the actual relevant files before suggesting exact edits. Do not assume that the server is online or that previous fixes were verified.

Some LLMs cannot browse GitHub or private repositories. Attach these Markdown files or paste their contents instead; a repository URL alone does not guarantee access.

## How to read the mirror

`server/home/tabahi/kdg-dev/...` represents `/home/tabahi/kdg-dev/...` on the Linux host. Files inside `server/` contain descriptions only. `_CONTEXT.md` keeps an otherwise empty folder in Git and explains its role. It is **not a file known to exist on the real server**.

- Python, TypeScript, configuration, and state filenames are represented by unmistakable placeholders.
- Actual binary filenames use `.placeholder.md` instead of fake binary contents.
- Usernames in directory paths are part of the known layout, not proof that every user's workspace exists.
- Build dependencies and outputs are represented by folder notes, not committed artifacts.
- Unknown Compose, Docker volume, and playit configuration paths are **not invented**.

### Evidence and limitations

Reconstructed on **2026-11-13** from prior deployment records and saved local source copies while the server was reported offline. There was no fresh remote filesystem scan. Detailed directories beneath runtime data are conditional examples, not observed contents. See [CONTEXT_METADATA.json](CONTEXT_METADATA.json).

No passwords, tokens, real user-state files, uploads, world data, repositories, notebooks, logs, or source code were copied into this repository.

## Check and maintain

Run `python scripts/validate_context.py` before committing. The check validates this context package, not the real server.

When the server is available, confirm paths using targeted read-only inspection. Update the context date, evidence, tree, and placeholders together. Never upload runtime data or credentials to make the map more complete.
