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

def run_raw(text):
    return subprocess.run([sys.executable, str(HOOK)], input=text, capture_output=True, text=True).returncode

def test_garbage_stdin_blocked(): assert run_raw("not json") == 2
def test_empty_stdin_blocked(): assert run_raw("") == 2
def test_json_without_file_path_blocked(): assert run_raw("{}") == 2                      # fails closed
def test_tool_input_without_file_path_blocked(): assert run_raw('{"tool_input":{}}') == 2
def test_tool_input_not_a_dict_blocked(): assert run_raw('{"tool_input":"x"}') == 2
def test_traversal_blocked(): assert code("/w/notes/../protected/fees.csv") == 2

def test_symlink_into_protected_blocked(tmp_path):
    (tmp_path / "protected").mkdir()
    (tmp_path / "notes").mkdir()
    (tmp_path / "notes" / "shortcut").symlink_to(tmp_path / "protected")
    ev = {"cwd": str(tmp_path), "tool_input": {"file_path": "notes/shortcut/x.csv"}}
    assert subprocess.run([sys.executable, str(HOOK)], input=json.dumps(ev), capture_output=True, text=True).returncode == 2
