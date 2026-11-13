# Recorded server directory map

Prepared 2026-11-13, offline. This is a **selected path map**, not a complete live listing. The mirror in `server/` contains placeholders only. `_CONTEXT.md` files are repository notes and are not real-server files.

## Application and data paths

```text
/home/tabahi/
├── .nvm/versions/node/v26.13.0/                 # previously used build runtime
├── kdg-ui-pre-glass-20261112.tar.gz            # recorded snapshot, contents omitted
└── kdg-dev/
    ├── KDG_SERVER_COMMANDS.md
    ├── MINECRAFT_SERVER_GUIDE.md
    ├── kdg-api/
    │   ├── .venv/                            # installed environment omitted
    │   ├── requirements.txt
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── auth.py
    │   │   ├── apikeys.py
    │   │   ├── audit.py
    │   │   ├── docker_readonly.py
    │   │   ├── modules_extra.py
    │   │   ├── terminal.py
    │   │   ├── userusage.py
    │   │   ├── s3store.py
    │   │   ├── minecraft.py
    │   │   ├── minecraft_extra.py
    │   │   ├── mcbackup.py
    │   │   ├── playit.py
    │   │   ├── workspaces.py
    │   │   ├── jupyter_proxy.py
    │   │   └── drive/
    │   │       ├── __init__.py
    │   │       ├── router.py
    │   │       ├── schemas.py
    │   │       ├── nextcloud.py
    │   │       └── video.py
    │   ├── kdg-auth-users.json
    │   ├── kdg-sessions.json
    │   ├── kdg-api-keys.json
    │   ├── kdg-audit.jsonl
    │   ├── kdg-attribution.json
    │   ├── kdg-user-map.json
    │   ├── kdg-nc-sso-map.json
    │   ├── kdg-cache/previews/                # cache, not main Drive storage
    │   └── kdg-s3/
    │       └── <bucket-name>/<object-path>   # conditional runtime data
    ├── kdg-frontend/
    │   └── cloud-command-center-main/       # canonical frontend source
    │       ├── package.json
    │       ├── tsconfig.json
    │       ├── vite.config.ts
    │       ├── components.json
    │       ├── node_modules/                 # generated dependencies omitted
    │       ├── public/kdg-logo.png
    │       ├── src/
    │       │   ├── components/
    │       │   │   ├── charts/
    │       │   │   ├── dialogs/
    │       │   │   ├── kdg/
    │       │   │   │   ├── primitives.tsx
    │       │   │   │   └── terminal-dock.tsx
    │       │   │   ├── layout/app-sidebar.tsx
    │       │   │   └── ui/
    │       │   ├── hooks/use-session.tsx
    │       │   ├── lib/
    │       │   ├── routes/                    # selected recorded pages only
    │       │   │   ├── __root.tsx
    │       │   │   ├── index.tsx
    │       │   │   ├── login.tsx
    │       │   │   ├── minecraft.tsx
    │       │   │   ├── minecraft.$id.tsx
    │       │   │   ├── kdg-drive.tsx
    │       │   │   ├── terminal.tsx
    │       │   │   ├── lab.tsx
    │       │   │   ├── workspace.tsx
    │       │   │   └── user-usage.tsx
    │       │   ├── services/
    │       │   │   ├── api/
    │       │   │   │   ├── client.ts
    │       │   │   │   └── queries.ts
    │       │   │   └── mocks/                 # development fixtures only
    │       │   ├── test/
    │       │   ├── types/index.ts
    │       │   ├── utils/
    │       │   ├── router.tsx
    │       │   ├── routeTree.gen.ts
    │       │   ├── server.ts
    │       │   ├── start.ts
    │       │   └── styles.css
    │       └── .output/                      # generated production output
    │           ├── public/assets/
    │           └── server/
    ├── minecraft/
    │   ├── servers.json
    │   ├── data/
    │   │   ├── kdg-smp-bcf0bb/               # recorded KDG SMP path
    │   │   └── <other-server-id>/            # conditional, names unknown
    │   ├── backups/
    │   │   └── <server-id>/                  # conditional, contents unverified
    │   │       ├── <id>-<timestamp>.tar.gz
    │   │       └── pre-restore-<timestamp>/
    │   └── .kdg-backup/
    │       ├── settings.json
    │       ├── <server-id>.json              # conditional per-server settings
    │       └── rclone.conf                   # conditional authorization
    └── workspaces/
        ├── tabahi/                           # recorded workspace slug
        ├── parth/                            # recorded workspace slug
        └── <other-user-slug>/                 # created on demand
            ├── notebooks/
            ├── repos/<repository-name>/
            ├── drive/
            └── .kdg/
                ├── workspace.json
                ├── git-credentials.json     # conditional
                ├── git-credentials-store    # conditional
                ├── drive.json               # conditional
                └── rclone.conf              # conditional
```

The illustrated workspace subfolders also apply to `tabahi/` and `parth/`; see [WORKSPACE_LAYOUT.md](WORKSPACE_LAYOUT.md). Names in angle brackets are templates, not literal directories. Current existence of optional runtime files is unverified.

## Host configuration and helpers

```text
/
├── opt/kdg/config/traefik/                    # exact filenames unknown
├── etc/
│   ├── kdg-api-nextcloud.env
│   ├── kdg/KDG_SERVER_COMMANDS.md
│   ├── profile.d/99-kdg-home.sh
│   ├── udev/rules.d/90-kdg-ac-backup.rules
│   └── systemd/system/
│       ├── kdg-api.service
│       ├── kdg-api.service.d/
│       │   ├── minecraft.conf
│       │   └── workspaces.conf
│       ├── kdg-frontend.service
│       ├── kdg-mc-backup.service
│       ├── kdg-mc-backup.timer
│       ├── kdg-mc-shutdown-save.service
│       ├── rtc-sync.service
│       └── rtc-sync.timer
├── usr/local/bin/
│   ├── kdg
│   ├── kdg-home
│   └── kdg-mc-emergency-save
└── var/log/kdg-mc-emergency-save.log
```

Other system files/units may exist; packaged services can install units outside `/etc/systemd/system`. Binary/archive/log filenames in this tree are represented by `.placeholder.md` notes in the repository.

## Container mount map

| Container | Linux host directory | Container path |
|---|---|---|
| `mc-kdg-smp-bcf0bb` | `/home/tabahi/kdg-dev/minecraft/data/kdg-smp-bcf0bb/` | `/data` |
| `mc-<server-id>` | `/home/tabahi/kdg-dev/minecraft/data/<server-id>/` | `/data` |
| `ws-tabahi` | `/home/tabahi/kdg-dev/workspaces/tabahi/` | `/home/jovyan/work` |
| `ws-parth` | `/home/tabahi/kdg-dev/workspaces/parth/` | `/home/jovyan/work` |

These paths do not imply the containers are currently running. Nextcloud/database volume mounts and Docker data-root are unknown; do not assume `/var/lib/docker` is the configured storage root.
