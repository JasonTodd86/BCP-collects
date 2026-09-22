#!/usr/bin/env python3
"""Print Facebook-ready text for a Sunday's collect from the 2019 ACNA BCP.

Usage:
    python3 scripts/get_collect.py                # next upcoming Sunday
    python3 scripts/get_collect.py 2027-03-28      # a specific Sunday

Exits non-zero (with an explanatory message on stderr) if no collect text
has been entered yet for that Sunday in data/collects.json.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bcp_calendar import describe_sunday  # noqa: E402

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "collects.json"


def next_sunday(today: date) -> date:
    if today.weekday() == 6:
        return today
    return today + timedelta(days=(6 - today.weekday()) % 7)


def main() -> int:
    if len(sys.argv) > 1:
        target = date.fromisoformat(sys.argv[1])
        if target.weekday() != 6:
            print(f"error: {target} is not a Sunday", file=sys.stderr)
            return 2
    else:
        target = next_sunday(date.today())

    info = describe_sunday(target)
    entries = json.loads(DATA_PATH.read_text())
    entry = entries.get(info.key)

    if entry is None:
        print(
            f"error: no data/collects.json entry for key '{info.key}' "
            f"({info.title}, {target.isoformat()})",
            file=sys.stderr,
        )
        return 1

    title = entry.get("title") or info.title
    text = entry.get("text")

    if not text:
        print(
            f"error: no collect text yet for '{title}' ({target.isoformat()}, "
            f"key: {info.key}). Add it to data/collects.json.",
            file=sys.stderr,
        )
        return 1

    subject = "the " + title[4:] if title.startswith("The ") else title
    post = f"{text}\n\n- Collect for {subject}, Book of Common Prayer"
    print(post)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
