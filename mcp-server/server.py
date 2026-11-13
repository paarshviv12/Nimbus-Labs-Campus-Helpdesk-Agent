#!/usr/bin/env python3
"""Campus helpdesk MCP server (stdio). MOCK DATA ONLY.

Built with the official MCP Python SDK v2 (`mcp` on PyPI): MCPServer, @tool, @resource.
IMPORTANT: on stdio, stdout is reserved for MCP messages. Never print() to stdout here.
"""
import csv
import json
import re
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field
from typing import Annotated

HERE = Path(__file__).parent
DATA = HERE / "data"

mcp = MCPServer(
    "campus-helpdesk",
    instructions="Read-only campus helpdesk. Answers come only from the mock data files.",
)

DAY_ALIASES = {
    "mon": "Mon", "monday": "Mon", "tue": "Tue", "tues": "Tue", "tuesday": "Tue",
    "wed": "Wed", "wednesday": "Wed", "thu": "Thu", "thur": "Thu", "thursday": "Thu",
    "fri": "Fri", "friday": "Fri", "sat": "Sat", "saturday": "Sat",
}
BATCH_RE = re.compile(r"^[A-Za-z][0-9]$")      # e.g. A1, B2
STUDENT_RE = re.compile(r"^S[0-9]{4}$")         # e.g. S1001


@mcp.tool()
def get_timetable(
    batch: Annotated[str, Field(description="Batch code: one letter and one digit, e.g. A1")],
    day: Annotated[str, Field(description="Weekday: Mon, Tue, Wed, Thu, Fri or Sat (full names also work)")],
) -> str:
    """Return the timetable rows for one batch (like A1) on one day (like Mon or Monday), from the mock timetable CSV. Read-only."""
    if not BATCH_RE.match(batch.strip()):
        raise ToolError(f"Invalid batch '{batch}'. Expected a letter and a digit, like A1.")
    key = DAY_ALIASES.get(day.strip().lower())
    if key is None:
        raise ToolError(f"Invalid day '{day}'. Use Mon, Tue, Wed, Thu, Fri or Sat.")
    with open(DATA / "timetable.csv", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f)
                if r["batch"].upper() == batch.strip().upper() and r["day"] == key]
    if not rows:
        return f"NOT FOUND: no timetable rows for batch={batch.strip().upper()}, day={key}"
    lines = ["batch,day,start_time,end_time,subject,room,faculty"]
    lines += [",".join(r[c] for c in ("batch", "day", "start_time", "end_time", "subject", "room", "faculty"))
              for r in rows]
    return "\n".join(lines)


@mcp.tool()
def get_fee_status(
    student_id: Annotated[str, Field(description="Mock student ID: S followed by 4 digits, e.g. S1001")],
) -> str:
    """Return the mock fee status (total due, paid, status) for one student ID like S1001. Read-only; mock data only."""
    sid = student_id.strip().upper()
    if not STUDENT_RE.match(sid):
        raise ToolError(f"Invalid student_id '{student_id}'. Expected S followed by 4 digits, like S1001.")
    fees = json.loads((DATA / "fees.json").read_text(encoding="utf-8"))
    rec = fees.get(sid)
    if rec is None:
        raise ToolError(f"No fee record for student_id {sid}.")
    return json.dumps({"student_id": sid, **rec})


@mcp.resource("hostel://rules", name="hostel-rules", mime_type="text/markdown",
              description="Hostel rules (mock data).")
def hostel_rules() -> str:
    return (DATA / "hostel_rules.md").read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")
