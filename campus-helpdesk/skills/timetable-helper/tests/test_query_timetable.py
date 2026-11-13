"""Tests for scripts/query_timetable.py. Run: python3 -m pytest -q campus-helpdesk/skills/timetable-helper/tests"""
import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "query_timetable.py"

def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

def test_found_exit_0():
    r = run("--batch", "B1", "--day", "Wed", "--subject", "DBMS")
    assert r.returncode == 0 and "R-302" in r.stdout

def test_adversarial_class_not_in_csv_is_not_found():
    r = run("--batch", "B2", "--day", "Fri", "--subject", "Quantum Computing")
    assert r.returncode == 1 and "NOT FOUND" in r.stdout

def test_bad_day_exit_2():
    assert run("--batch", "A1", "--day", "Funday").returncode == 2
