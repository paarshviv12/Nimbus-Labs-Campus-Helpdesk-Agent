#!/usr/bin/env python3
"""Filter timetable.csv by batch and day (optionally subject).

Exit codes: 0 = rows found, 1 = NOT FOUND, 2 = bad input or missing file.
Standard library only.
"""
import argparse
import csv
import sys
from pathlib import Path

DAYS = {"mon": "Mon", "monday": "Mon", "tue": "Tue", "tues": "Tue", "tuesday": "Tue",
        "wed": "Wed", "wednesday": "Wed", "thu": "Thu", "thur": "Thu", "thurs": "Thu", "thursday": "Thu",
        "fri": "Fri", "friday": "Fri", "sat": "Sat", "saturday": "Sat"}
DEFAULT_CSV = Path(__file__).resolve().parent.parent / "data" / "timetable.csv"


def main() -> int:
    p = argparse.ArgumentParser(description="Look up classes in the timetable CSV.")
    p.add_argument("--batch", required=True, help="e.g. A1")
    p.add_argument("--day", required=True, help="e.g. Mon or Monday")
    p.add_argument("--subject", help="optional subject filter (case-insensitive substring)")
    p.add_argument("--csv", default=str(DEFAULT_CSV), help="path to timetable CSV")
    a = p.parse_args()

    day = DAYS.get(a.day.strip().lower())
    if day is None:
        print(f"ERROR: unknown day '{a.day}'. Use Mon-Sat.", file=sys.stderr)
        return 2
    try:
        with open(a.csv, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except OSError as e:
        print(f"ERROR: cannot read CSV: {e}", file=sys.stderr)
        return 2

    batch = a.batch.strip().upper()
    hits = [r for r in rows if r["batch"].upper() == batch and r["day"] == day]
    if a.subject:
        s = a.subject.strip().lower()
        hits = [r for r in hits if s in r["subject"].lower()]

    if not hits:
        extra = f", subject~'{a.subject}'" if a.subject else ""
        print(f"NOT FOUND: no rows for batch={batch}, day={day}{extra}")
        return 1
    print("batch,day,start_time,end_time,subject,room,faculty")
    for r in hits:
        print(",".join(r[c] for c in ["batch", "day", "start_time", "end_time", "subject", "room", "faculty"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
