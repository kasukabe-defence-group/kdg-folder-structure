# KDG Cloud: context for an LLM

## Trust boundary

This is a reconstructed **architecture and path map**, not live source code or a server inventory. Prepared 2026-11-13 while the server was reported offline. `server/` contains descriptions and placeholders only. A feature described as previously deployed is not proof that it currently works. Ask for actual files and test output before changing anything.

## What the system does

KDG Cloud is a dashboard for a Linux host: resources, processes, containers, real Nextcloud Drive, terminal sessions, Minecraft servers, and per-user JupyterLab/Git/Google Drive workspaces.

- **Frontend:** React, TanStack Start/Router, TanStack Query, Vite, Tailwind and shared UI components. Runs as host systemd service `kdg-frontend`.
- **Backend:** Python/FastAPI, psutil, server-side Docker commands, persistent JSON state. Runs as host systemd service `kdg-api`.
- **Routing:** Traefik fronts the dashboard and `/api/v1`; `/drive/` serves the Nextcloud UI. Browser API requests use the same origin. Host API/frontend addresses previously used `172.19.0.1:8000` and `172.19.0.1:8081`; recheck networking before use.
- **Containers:** Nextcloud and its supporting stack, Traefik, GET-only Docker socket proxy, Minecraft instances, and Jupyter workspaces. Exact Compose and volume locations are unknown here.
- **Network:** LAN/Tailscale access; public dashboard HTTPS via Tailscale Funnel. Funnel does not expose Minecraft TCP. playit.gg provides a separate public Minecraft tunnel after the user configures one.
- **Hardware last reported:** eight logical CPUs, approximately 7.13 GiB RAM, NVIDIA GTX 1050 with 4 GiB VRAM. NVENC H.264/HEVC was previously tested. These are historical observations, not current measurements.

## Main host paths

| Path | Purpose |
|---|---|
| `/home/tabahi/kdg-dev/kdg-api/` | Backend code, Python environment, authentication/session/key/audit state, preview cache and filesystem-backed object storage |
| `/home/tabahi/kdg-dev/kdg-frontend/cloud-command-center-main/` | Canonical dashboard source and `.output/` production build |
| `/home/tabahi/kdg-dev/minecraft/` | Server registry, per-server data, local backups and backup authorization/configuration |
| `/home/tabahi/kdg-dev/workspaces/<user-slug>/` | Persistent notebooks, cloned repositories, optional Drive mirror and private workspace settings |
| `/opt/kdg/config/traefik/` | File-provider reverse-proxy configuration; exact filenames not recorded |
| `/etc/kdg-api-nextcloud.env` | Server-only Nextcloud environment settings; no values stored here |
| `/etc/systemd/system/` | Recorded KDG units and drop-ins; other units may be elsewhere |
| `/usr/local/bin/kdg*` | Login homescreen/command helpers and emergency Minecraft save helper |

## Authentication and ownership

Recorded dashboard roles: `tabahi` (owner), `Yuuta` and `Parth` (admins), `Light` and `Razor` (moderators). Directory slugs are lowercase. These dashboard accounts are not proof of separate Linux accounts.

- Protect `/api/v1/*` except designated public authentication/health operations.
- Passwords use scrypt hashes; persisted sessions store token digests, not plaintext cookies.
- API keys are show-once `kdg_*` values, stored as SHA-256 hashes with scopes, rate limits and audit records.
- Resource ownership comes from `kdg.owner` container labels, registered terminal PID trees, explicit admin mappings or meaningful OS-account evidence. Anything unresolved must remain `unattributed`.
- Per-process psutil CPU percentages and host CPU percentages have different scales. The previously claimed CPU normalization fix **was not established by successful patch output in the available record**. Inspect current `userusage.py` and the UI before assuming it is fixed.

## Drive

- Real path: **browser -> FastAPI -> Nextcloud** using server-owned credentials and WebDAV/OCS. No browser credentials or mock fallback in production.
- Dashboard route is `/kdg-drive`; Nextcloud's own UI is `/drive/`.
- Features previously deployed: uploads, cancellation, multi-select, shares/public links, previews, trash and image compression before upload.
- Video processing is server-side ffmpeg **only on explicit request** at `POST /api/v1/drive/video/process`. Options include compression, codec/quality, bitrate, scaling, FPS, audio, trim/crop and format. NVENC may be selected when available. No background transcoding by default.
- API `kdg-cache/previews/` is a cache, **not Nextcloud file storage**. Real Drive storage resides in Nextcloud's persistent storage, whose host mount path is not known here.

## Minecraft

- API prefix `/api/v1/minecraft`; management requires a moderator/admin/owner session.
- Each server uses `itzg/minecraft-server:latest`, container `mc-<server-id>`, restart policy `unless-stopped`, and labels `kdg.owner` / `kdg.managed=minecraft`.
- Host `minecraft/data/<server-id>/` mounts as `/data` inside the container. Config registry is `minecraft/servers.json`.
- A recorded server is `kdg-smp-bcf0bb`, named KDG SMP. Its last reported Minecraft state was stopped; current state is unknown.
- Dashboard pages: `/minecraft` and `/minecraft/<id>`. Tabs cover console/logs, players, worlds, plugins/mods, software, settings, backups and deletion.
- World changes require a stopped server. Existing API operations include create with seed/type, ZIP upload, activation, regeneration and deletion.
- Creation UI was reported deployed with random generation, seed/type, or an uploaded world. Generation occurs on first start; upload follows server creation while stopped. `level.dat` is required. Upload failure can leave the server record created, so do not blindly retry server creation.
- ZIP input limit in saved code: 4 GiB compressed, 12 GiB expanded. Full traversal/dimension-preservation validation should be inspected before trusting arbitrary archives; placeholders are not a security audit.
- Seed/type were added to the backend's saved server configuration and container environment. A persistent environment seed/type may interact with later Worlds-tab changes; verify actual behavior on a disposable server.
- RCON secrets remain server-side. Modrinth dependency resolution is not automatic.
- playit agent was previously connected/verified, but no confirmed public tunnel address was recorded. Creating the server does not automatically create a public tunnel.

## Backups and power

`minecraft/.kdg-backup/` holds configuration and optional rclone authorization; `minecraft/backups/<id>/` holds tarballs and pre-restore stashes.

- Intended triggers: every 10 minutes, before stop/restart, before shutdown, and charger unplug.
- Intended consistent-save sequence: RCON `save-off -> save-all flush -> snapshot -> save-on`.
- Restore-on-start may rewind the world to the newest remote backup and stash current data. Do not enable or invoke restoration casually; unbacked progress can be lost.
- **Unresolved:** a live backup test reported incorrect running-state detection; the helper may pass a container name to a function expecting a server ID. Real save-flush consistency requires re-verification.
- **Unresolved:** real Google Drive backup/upload/retention/restore awaits user OAuth authorization. A local-remote stand-in test is not proof of successful real Drive backups.
- Battery/RTC problems were reported. Instant power loss cannot guarantee an emergency save or upload. Software clock mitigation (`fake-hwclock`, `rtc-sync`) is not a substitute for a battery/UPS.

## Workspaces and JupyterLab

- Host `workspaces/<user-slug>/` mounts as `/home/jovyan/work` in `ws-<user-slug>`.
- Expected subfolders: `notebooks/`, `repos/`, `drive/`, `.kdg/`. Runtime creation is on demand; not all user folders necessarily exist.
- Workspace containers use the Jupyter scipy-notebook image, configurable memory/vCPU/GPU, ownership labels and persistent data.
- `/lab` embeds Jupyter through `/api/v1/workspaces/jupyter/<slug>/`; the proxy injects authentication server-side. Owner/admin can access other users' Labs; other roles only their own.
- Git credentials and optional rclone Drive authorization are private workspace files. Connecting Drive needs user authorization.
- Leave-page warnings were added for active terminals, running Jupyter sessions and Drive uploads. A browser warning is not a data durability guarantee.

## Frontend, deployment, and current risks

- Most recent requested visual direction: dark neutral black/white/grey, minimal rounding; custom server emblem used for sidebar/login/favicon. Prior glass/noir styling notes are historical and may conflict with the latest source.
- Editable local frontend was `D:\Contributions\Kdg\work\ccm`; deploy target is the canonical Linux frontend path above. The older local `kdg-frontend/src` mirror is stale and must not be used for deployment.
- Build uses Node v26.13.0 and Vite, then restarts `kdg-frontend`. Backend changes require Python syntax/tests and restarting `kdg-api`.
- A successful HTTP 200 or Vite build alone does not prove browser hydration, authentication, or a feature works.
- Dashboard previously remained stuck on “Checking dashboard session” despite server health and repeated rebuilds. A 10-second fallback was added, but resolution was not confirmed. Stray files from misdirected SCP were previously associated with broken client builds. Inspect current source and shipped asset references rather than assuming a browser-cache issue.
- Previous TypeScript route-tree/type errors were reported. Verify the current type check rather than trusting earlier clean-build claims.

## Non-negotiable constraints

1. Preserve existing data, Nextcloud/Docker volumes, ownership controls and authentication.
2. Keep the Docker socket proxy GET-only; do not widen it to implement management operations.
3. Never embed credentials, secrets or raw upstream authorization in browser code.
4. Do not deploy these placeholders or use them to overwrite actual server files.
5. Obtain actual relevant files and fresh evidence before edits. Record what was tested, not what was merely intended.

## Unknown details to ask for

Current service status, complete source/config contents, actual Compose path, Docker data-root and volume mounts, all server/workspace IDs, playit tunnel address, backup authorization/health, and current browser console/network evidence.
