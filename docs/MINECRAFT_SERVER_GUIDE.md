# Minecraft creation options explained

This describes the recorded KDG UI. It does not verify the current deployment. Most settings are changed while the server is stopped.

| Option | Meaning and practical advice |
|---|---|
| Server name | Dashboard display name, also used to derive a unique internal ID. Example: `Parth Survival`. |
| Description | Optional note for administrators; it does not install mods or change gameplay. |
| Server software | **Vanilla:** plain Java Minecraft. **Paper/Spigot:** plugin servers. **Purpur:** Paper-compatible with extra configuration. **Fabric/Forge/NeoForge:** mod loaders; clients generally need matching versions and required mods. Mods and plugins are not interchangeable. |
| Minecraft version | Minecraft release to run. `LATEST` is a moving target; pin a version for modpacks and established worlds. Back up before upgrades and avoid opening a newer world in an older release. |
| Memory | Java memory setting, e.g. `2G` for roughly 2 GiB. It is **not automatically a hard container memory limit**: saved Docker arguments did not set `--memory`. Java and the container can use additional native memory. The host's RAM is shared by all services. |
| Port (TCP) | Host port for Minecraft Java, normally `25565`, mapped to container port `25565`. Each managed server needs its own host port. A playit tunnel must target that port separately. |
| Max players | Admission cap, not a promise that the hardware can sustain that many players. Default 20. |
| Difficulty | Peaceful, easy, normal or hard; changes hostile mobs and survival difficulty. |
| MOTD | “Message of the Day”: text shown beneath the server entry in a player's multiplayer list. |
| Game mode | Default mode: survival, creative, adventure or spectator. Existing player modes may need separate changes. |
| PvP | Whether players can damage one another. Plugins can impose additional rules. |
| Online mode | Authenticates player accounts. Keep it on for public servers. Turning it off permits unauthenticated identities and can enable impersonation without additional protection; it does not mean the server is offline. |
| RCON console | Remote command channel used by dashboard operations and intended backup save flushes. Keep enabled for those workflows. It is not a player connection port and should not be publicly exposed. |
| RCON password | Leave blank for generation. It is private server-side state and must not appear in this context repository. |
| World seed | Text or number used for new terrain generation. Blank means random. Reproducing terrain requires compatible Minecraft version, generator and settings as well as the seed. Changing a seed does not replace existing terrain. |
| World type | Normal, Superflat, Large biomes, Amplified, or the recorded Single biome option. Support/settings vary by release; Amplified terrain can cost more resources. |
| Upload world ZIP | Loads an existing Java world instead of generating a fresh one. The ZIP must contain `level.dat` at its root or in one immediate world folder. Use compatible software/version. Bedrock worlds require conversion first. |
| Uploaded world name | Destination folder name on the server, optionally derived from the ZIP filename. It is not a path to find inside the archive. |
| Create server | Creates the stopped server record/configuration; the recorded workflow then uploads the chosen ZIP, if any. It does not start the server or automatically create a public tunnel. |
| Cancel | Dismisses creation before submission. Do not assume closing a browser cancels a request already accepted by the backend. |

## Three initial-world choices

1. **Automatic/random:** no upload and blank seed; generate on first start.
2. **Specified seed:** no upload, enter a seed and select a type; generate on first start.
3. **Existing world:** choose a ZIP; upload after creating the server, keep it stopped until upload finishes, then start to load it.

The first start also downloads required server software and can take several minutes. Seed/type inputs were disabled when a ZIP was selected in the recorded UI; verify the actual request because disabled controls can retain state.

The saved upload API accepts up to 4 GiB compressed and 12 GiB expanded. Validate archives and ensure adequate free disk space. Do not assume separate Paper Nether/End folders were preserved by an upload without checking the archive and implementation.

## After creation

- Manage console, players, worlds, plugins/mods, software, settings and backups from the server page.
- Stop before world changes. Regeneration and deletion can destroy world progress; take a verified backup first.
- Configure a Minecraft Java/TCP tunnel in playit.gg separately and share its assigned address. The HTTPS dashboard URL is not a Minecraft address.
- Drive backup authorization and running-world consistency still require verification; automatic backup intent is not a proven recovery guarantee.
