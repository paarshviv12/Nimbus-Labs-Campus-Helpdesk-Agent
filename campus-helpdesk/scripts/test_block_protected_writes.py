"""Run: python3 -m pytest -q campus-helpdesk/scripts/test_block_protected_writes.py"""
import json, subprocess, sys
from pathlib import Path
HOOK = Path(__file__).with_name("block_protected_writes.py")

def code(path):
    ev = {"cwd": "/w", "tool_input": {"file_path": path}}
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(ev), capture_output=True, text=True).returncode

def test_blocked(): assert code("/w/protected/a.csv") == 2
def test_allowed(): assert code("/w/notes/a.md") == 0
def test_mixed_case_blocked(): assert code("/w/Protected/a.csv") == 2      # the bug
def test_name_only_allowed(): assert code("/w/protected.txt") == 0
