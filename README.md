# Building and Auditing an AI-Agent Toolchain (ASSIGNMENT_8)

Paarshvi Vijoy | Roll no 150096725188 | Cohort: Jeff Bezos | AI Tools and Prompt Engineering

Mock data only. Contents:

| Path | What it is |
|---|---|
| `timetable-helper/` | Part B skill (SKILL.md, references/, scripts/, data/) |
| `campus-helpdesk/` | Part C plugin: skill copy, `/timetable` command, write-guard hook, `.mcp.json` |
| `.claude-plugin/marketplace.json` | Part C marketplace entry |
| `THREAT_MODEL.md` | Part C threat model |
| `mcp-server/` | Part D stdio MCP server (official Python SDK), tests, annotated trace |
| `logs/` | Real command output for Parts B to E |
| `docs/` | The PDF report and the prompt log |

Branches (Part E): `main`, `bugfix/hook-path`, `feature/mcp-server`, `feature/skill-tests`.

## Run

```bash
# Part B script
python3 timetable-helper/scripts/query_timetable.py --batch A1 --day Mon

# Part C hook + skill tests
python3 -m pytest -q campus-helpdesk/scripts campus-helpdesk/skills/timetable-helper/tests

# Part D server and tests
pip install "mcp>=2,<3" pytest
python3 mcp-server/server.py            # stdio server, waits for a client
python3 -m pytest -v mcp-server/tests   # 10 tests
```

Plugin steps (validate, add marketplace, install, list, uninstall) are in the report, Part C.3.
In `campus-helpdesk/.mcp.json` the server path is a placeholder; see `mcp-server/README.md` for the one-line swap.
