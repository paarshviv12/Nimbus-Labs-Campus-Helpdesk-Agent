# campus-helpdesk MCP server (stdio, mock data only)

A small read-only MCP server built with the official MCP Python SDK (`mcp` on PyPI, v2 line, tested with 2.3.0).

| Kind | Name | What it does |
|---|---|---|
| Tool | `get_timetable(batch, day)` | Rows from `data/timetable.csv`; returns `NOT FOUND: ...` if nothing matches |
| Tool | `get_fee_status(student_id)` | Mock record from `data/fees.json` (IDs S1001 to S1003) |
| Resource | `hostel://rules` | Markdown from `data/hostel_rules.md` |

All data is mock data. There is no database and no SQL. Inputs are validated by regex before any file is read.

## Run

```bash
pip install --break-system-packages "mcp[cli]"     # install line from py.sdk.modelcontextprotocol.io
python3 server.py                                   # speaks JSON-RPC on stdin/stdout; waits for a client
```

## Test

```bash
python3 -m pytest -v tests/test_server.py   # 10 tests: tools, failures, description lint, stdout purity
python3 tests/trace_client.py               # raw JSON-RPC trace -> logs/trace.jsonl
```

Logs from my run are in `logs/` (`pytest_run.txt`, `trace_run.txt`, `trace.jsonl`). The annotated trace is `ANNOTATED_TRACE.md`.

## Wire it into the plugin

`campus-helpdesk/.mcp.json` starts a bundled copy of this server through the plugin root variable:

```json
{ "mcpServers": { "campus-helpdesk-mcp": { "command": "python3", "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-server/server.py"] } } }
```

The bundled copy (`campus-helpdesk/mcp-server/`) must match this folder; `campus-helpdesk/scripts/test_copies_in_sync.py` fails if they drift. The server needs `pip install "mcp>=2,<3"` on the machine.

## Check with the official MCP Inspector

```bash
npx -y @modelcontextprotocol/inspector --cli python3 server.py --method tools/list
npx -y @modelcontextprotocol/inspector --cli python3 server.py --method tools/call --tool-name get_fee_status --tool-arg student_id=S9999
```

Output is in `../logs/partD_inspector.txt` (the S9999 call is the failure case and returns `isError: true`).

## Design rules

- stdout carries only MCP messages (stdio rule); nothing here prints to stdout.
- Anticipated failures raise the SDK's `ToolError`, so the model sees a readable message.
- Tool descriptions are plain text, short, and linted in tests for injection-style phrases.
- `@nimbus/mcp-skill-bridge` is not used: it does not exist on npm (`npm view` returned E404 on 13 Nov 2026).
