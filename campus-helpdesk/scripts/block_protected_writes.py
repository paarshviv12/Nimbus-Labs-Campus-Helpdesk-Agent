#!/usr/bin/env python3
"""PreToolUse hook: block Write/Edit calls whose target is inside a `protected/` folder.

Reads the hook JSON from stdin. Exit 2 + message on stderr = block the tool call
(documented PreToolUse behaviour). Exit 0 with no output = no decision (normal flow).
Fails closed: if the input is unreadable, or has no file path to judge, the call is blocked
(this hook is only attached to Write and Edit, which always carry a file path).
"""
import json
import os
import sys

PROTECTED_DIR_NAME = "protected"


def main() -> int:
    try:
        event = json.load(sys.stdin)
        path = event.get("tool_input", {}).get("file_path") or ""
    except Exception as exc:  # unreadable input -> fail closed
        print(f"Blocked: hook could not parse its input ({exc}).", file=sys.stderr)
        return 2

    if not isinstance(path, str) or not path:
        print("Blocked: hook found no file_path to check in the tool input.", file=sys.stderr)
        return 2  # cannot judge the target -> fail closed

    base = event.get("cwd") or os.getcwd()
    resolved = os.path.realpath(os.path.join(base, path))  # collapses '..' and symlinks
    parts = resolved.split(os.sep)

    if PROTECTED_DIR_NAME in [p.casefold() for p in parts[:-1]]:
        print(
            f"Blocked by campus-helpdesk hook: '{path}' is inside a protected folder "
            f"({resolved}). Ask the user to make this change manually.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
