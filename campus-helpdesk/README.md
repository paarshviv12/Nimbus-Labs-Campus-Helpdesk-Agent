# campus-helpdesk (Claude Code plugin)

Mock-data plugin for the Nimbus Campus Helpdesk assignment. It bundles:

- skill `timetable-helper`: answers class timing, room and faculty questions only from a mock timetable CSV, via a helper script
- command `/campus-helpdesk:timetable`: asks for batch and day, then uses the skill
- hook (PreToolUse on Write and Edit): blocks writes to any `protected/` folder
- `.mcp.json`: one MCP server entry that runs the bundled mock-data server `mcp-server/server.py` (needs `pip install "mcp>=2,<3"`; the copy is kept identical to the top-level `mcp-server/` by a test)

Install: add the marketplace folder, then run `claude plugin install campus-helpdesk@nimbus-campus-marketplace`. All data is mock data.
