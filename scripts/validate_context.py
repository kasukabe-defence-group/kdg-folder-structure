"""Check the descriptive context package; never contact or modify the real server."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DOCS = (
    "README.md", "AGENTS.md", "LLM_CONTEXT.md", "SERVER_TREE.md",
    "WORKSPACE_LAYOUT.md", "CONTEXT_METADATA.json", "docs/MINECRAFT_SERVER_GUIDE.md",
)
API = "server/home/tabahi/kdg-dev/kdg-api"
WEB = "server/home/tabahi/kdg-dev/kdg-frontend/cloud-command-center-main"
REQUIRED_PATHS = (
    "server/_CONTEXT.md", f"{API}/app/main.py", f"{API}/app/drive/video.py",
    f"{API}/kdg-auth-users.json", f"{API}/.venv/_CONTEXT.md",
    f"{WEB}/src/routes/minecraft.$id.tsx", f"{WEB}/src/hooks/use-session.tsx",
    f"{WEB}/node_modules/_CONTEXT.md", f"{WEB}/.output/public/assets/_CONTEXT.md",
    "server/home/tabahi/kdg-dev/minecraft/data/kdg-smp-bcf0bb/_CONTEXT.md",
    "server/home/tabahi/kdg-dev/minecraft/.kdg-backup/rclone.conf",
    "server/opt/kdg/config/traefik/_CONTEXT.md",
    "server/etc/kdg-api-nextcloud.env", "server/usr/local/bin/kdg-home",
    "server/var/log/kdg-mc-emergency-save.log.placeholder.md",
)
FORBIDDEN_SUFFIXES = {".png", ".jpg", ".mp4", ".zip", ".gz", ".pdf", ".log", ".ipynb", ".pem", ".key", ".db", ".pyc"}
SECRET_PATTERN = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|\bgh[pousr]_[A-Za-z0-9]{30,}\b"
    r"|\bgithub_pat_[A-Za-z0-9_]{40,}\b"
    r"|^\s*(?:export\s+)?(?:NEXTCLOUD_APP_PASSWORD|KDG_SUDO_PASSWORD|RCON_PASSWORD|GH_TOKEN|GITHUB_TOKEN)\s*=\s*\S+",
    re.MULTILINE,
)


def check_mirror_file(path, text):
    """Mirror JSON has only descriptive keys; executable/config placeholders are comments."""
    if path.suffix in {".json", ".jsonl"}:
        data = json.loads(text)
        if not isinstance(data, dict) or data.get("_placeholder") is not True:
            raise ValueError("JSON must have _placeholder: true")
        if set(data) != {"_placeholder", "purpose"} or not isinstance(data["purpose"], str):
            raise ValueError("JSON must contain only _placeholder and descriptive purpose")
    elif path.suffix == ".md":
        if not text.startswith("# PLACEHOLDER:"):
            raise ValueError("mirror Markdown must start with a placeholder heading")
    else:
        if "PLACEHOLDER:" not in text:
            raise ValueError("missing placeholder marker")
        if not all(not line.strip() or line.lstrip().startswith(("#", "//", "/*")) for line in text.splitlines()):
            raise ValueError("mirror code/config must contain comments only")
    if SECRET_PATTERN.search(text):
        raise ValueError("possible secret material")


def self_test():
    check_mirror_file(Path("state.json"), '{"_placeholder": true, "purpose": "State omitted"}')
    check_mirror_file(Path("main.py"), "# PLACEHOLDER: source omitted\n")
    for name, text in (
        ("state.json", '{"_placeholder": true, "token": "not-for-publication"}'),
        ("main.py", "# PLACEHOLDER: example\nprint('runnable code')\n"),
        ("rclone.conf", "# PLACEHOLDER: example\ntoken = actual-value\n"),
        ("note.md", "# PLACEHOLDER: example\nRCON_PASSWORD=not-for-publication\n"),
    ):
        try:
            check_mirror_file(Path(name), text)
        except ValueError:
            continue
        raise AssertionError(f"unsafe fixture was accepted: {name}")
    print("Self-tests: PASS (safe placeholders accepted, unsafe fixtures rejected)")


def main():
    try:
        if "--self-test" in sys.argv:
            self_test()
        for relative in REQUIRED_DOCS + REQUIRED_PATHS:
            if not (ROOT / relative).is_file():
                raise ValueError(f"missing required file: {relative}")
        metadata = json.loads((ROOT / "CONTEXT_METADATA.json").read_text(encoding="utf-8"))
        if metadata.get("liveFilesystemVerified") is not False:
            raise ValueError("offline provenance must remain explicit; update validator after a real inventory")
        mirror_files = sorted((ROOT / "server").rglob("*"))
        checked = 0
        for path in mirror_files:
            if path.is_symlink():
                raise ValueError(f"symlink in mirror: {path.relative_to(ROOT)}")
            if not path.is_file():
                continue
            if path.stat().st_size > 8192 or path.suffix in FORBIDDEN_SUFFIXES:
                raise ValueError(f"non-placeholder artifact: {path.relative_to(ROOT)}")
            check_mirror_file(path, path.read_text(encoding="utf-8"))
            checked += 1
        for slug in ("tabahi", "parth"):
            base = ROOT / "server/home/tabahi/kdg-dev/workspaces" / slug
            for folder in ("notebooks", "repos", "drive", ".kdg"):
                if not (base / folder).is_dir():
                    raise ValueError(f"workspace layout missing: {slug}/{folder}")
        for doc in REQUIRED_DOCS:
            if not doc.endswith(".md"):
                continue
            text = (ROOT / doc).read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if "://" not in target and not target.startswith("#"):
                    if not (ROOT / Path(doc).parent / target.split("#")[0]).exists():
                        raise ValueError(f"broken documentation link in {doc}: {target}")
        print(f"Checked {checked} mirror placeholders, required paths, workspace layout and document links.")
        print("VERDICT: PASS")
    except (ValueError, OSError, UnicodeError, AssertionError) as exc:
        print(f"VERDICT: FAIL -- {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
