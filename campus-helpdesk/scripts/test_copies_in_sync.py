"""The plugin ships its own copies of the Part B skill and the Part D server (a plugin must be
self-contained once installed). This test fails if a copy drifts from the canonical folder.
Run: python3 -m pytest -q campus-helpdesk/scripts/test_copies_in_sync.py"""
import filecmp
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PLUGIN = REPO / "campus-helpdesk"


def same(a: Path, b: Path):
    assert a.is_file() and b.is_file(), (a, b)
    assert filecmp.cmp(a, b, shallow=False), f"{a} differs from {b}"


def test_skill_copy_matches():
    canon = REPO / "timetable-helper"
    for f in canon.rglob("*"):
        if f.is_file() and "__pycache__" not in f.parts:
            same(f, PLUGIN / "skills" / "timetable-helper" / f.relative_to(canon))


def test_server_copy_matches():
    canon = REPO / "mcp-server"
    files = [canon / "server.py", canon / "requirements.txt"] + [f for f in (canon / "data").rglob("*") if f.is_file()]
    for f in files:
        same(f, PLUGIN / "mcp-server" / f.relative_to(canon))


def test_mcp_json_points_to_bundled_server():
    import json
    cfg = json.loads((PLUGIN / ".mcp.json").read_text(encoding="utf-8"))
    args = cfg["mcpServers"]["campus-helpdesk-mcp"]["args"]
    assert args == ["${CLAUDE_PLUGIN_ROOT}/mcp-server/server.py"]
    assert (PLUGIN / "mcp-server" / "server.py").is_file()
