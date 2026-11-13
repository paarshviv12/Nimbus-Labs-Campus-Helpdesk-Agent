---
description: Look up a batch's classes for a day from the campus timetable CSV (e.g. batch A1, Monday)
---

The student wants a timetable lookup. Use the `timetable-helper` skill to answer it.

- If the student did not give both a batch and a day, ask for the missing one before doing anything.
- Answer only from the script output and quote the matching rows.
- If nothing matches, reply exactly: "Not found in the timetable."
