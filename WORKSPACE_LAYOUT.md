# Per-user workspace layout

`<user-slug>` means the lowercase slug derived from the dashboard username. This is a conditional template, not an assertion that every workspace exists.

```text
/home/tabahi/kdg-dev/workspaces/<user-slug>/
├── notebooks/                # persistent notebooks and data
├── repos/
│   └── <repository-name>/    # cloned user repository
├── drive/                    # optional Google Drive mirror, not Nextcloud storage
└── .kdg/                     # private service settings (0700/0600 intended)
    ├── workspace.json        # runtime settings and private Jupyter token
    ├── git-credentials.json  # conditional Git authentication state
    ├── git-credentials-store # conditional Git credential-helper file
    ├── drive.json            # conditional Drive connection metadata
    └── rclone.conf           # conditional Drive authorization
```

The entire workspace is mounted as `/home/jovyan/work` in `ws-<user-slug>`. Access still depends on filesystem/container configuration; dashboard accounts are not equivalent to Linux users. Do not expose `.kdg` secrets through file APIs or public shares.
