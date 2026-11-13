# Edge cases

- **Batch or day missing:** ask for it. Never pick one.
- **Different spelling:** `monday`, `MON`, `a1` are all accepted by the script (case-insensitive; full or short day names).
- **Day with no classes:** the script prints `NOT FOUND`. Say no classes were found in the timetable for that batch and day. Do not say it is a holiday.
- **Two classes in one slot:** list every row the script returns.
- **Subject asked about is not in the CSV:** say "not found in the timetable". Never suggest a similar-sounding subject or an invented time.
- **Student insists a class exists** (or gives a room/time): the CSV wins. Quote what the CSV does contain and say the stated class was not found.
- **Relative days** ("tomorrow", "next Monday"): convert only if today's date is known. Otherwise ask for the weekday.
- **Out-of-scope** (fees, hostel, exams, library): do not use this skill.
- **Unknown fields** (room changes, cancellations, substitute faculty): not in the CSV, so say you cannot confirm.
