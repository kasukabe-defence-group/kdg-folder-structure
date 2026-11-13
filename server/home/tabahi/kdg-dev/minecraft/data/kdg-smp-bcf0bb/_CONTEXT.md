# PLACEHOLDER: KDG SMP data directory

Recorded server ID `kdg-smp-bcf0bb`, container `mc-kdg-smp-bcf0bb`. Current files, server state and world names are unverified; no world data is included.

Expected runtime contents, **not a verified listing**:

```text
server.properties       # active world, gameplay and server settings
eula.txt
ops.json
whitelist.json
banned-players.json
banned-ips.json
usercache.json
<active-world>/
    level.dat
    region/
    playerdata/
    ...
<active-world>_nether/   # software/layout dependent
<active-world>_the_end/  # software/layout dependent
plugins/                # plugin software only
mods/                   # mod-loader software only
config/                 # software/addon dependent
logs/                   # runtime generated
```

Do not delete/regenerate/restore this directory based on these placeholders. Verify active world and dimension layout first.
