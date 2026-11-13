# Instructions for agents reading this repository

- Read `LLM_CONTEXT.md`, `SERVER_TREE.md`, and `CONTEXT_METADATA.json` first.
- This repository is descriptive context only. Every file in `server/` is a placeholder; do not execute, deploy, or import it as real application code.
- Removing the leading `server/` produces the intended Linux host path. Paths inside container mount notes are container paths, not additional host directories.
- Do not infer that a placeholder or conditional runtime folder exists on the real server.
- The server was offline when this context was prepared. Prior summaries are not fresh verification, and unresolved bugs must stay unresolved until tested.
- Ask for the actual relevant source, configuration with secrets redacted, and runtime evidence before proposing exact fixes.
- Keep authentication on `/api/v1/*` except designated public auth/health paths. Never place credentials in frontend code.
- Preserve existing Nextcloud/Docker volumes, Minecraft worlds, workspace files, and socket-proxy GET-only restrictions. Do not suggest destructive migrations, resets, or broad cleanup.
- Do not commit credentials, real JSON state, RCON secrets, notebooks, world archives, cloned user repositories, logs, or generated binaries here.
- Context changes should retain clear provenance and uncertainty labels. Run `python scripts/validate_context.py` before committing.
