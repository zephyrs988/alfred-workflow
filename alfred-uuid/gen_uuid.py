#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alfred Script Filter: generate UUID (v4)."""

import json
import sys
import uuid
from datetime import datetime

ICON_PATH = "icon.png"


def item(title, subtitle="", arg=None, valid=True):
    value = arg if arg is not None else title
    row = {
        "uid": f"{title}-{subtitle}",
        "type": "default",
        "title": title,
        "subtitle": subtitle,
        "arg": str(value),
        "icon": {"path": ICON_PATH},
    }
    row["valid"] = bool(valid)
    return row


def emit(items):
    print(json.dumps({"items": items}, ensure_ascii=False))


def main():
    new_id = str(uuid.uuid4())
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emit(
        [
            item(
                new_id,
                f"UUID v4 · {now} · 回车复制",
                arg=new_id,
            ),
        ]
    )


if __name__ == "__main__":
    main()
