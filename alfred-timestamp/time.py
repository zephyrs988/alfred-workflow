#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alfred Script Filter: Unix timestamp <-> datetime conversion."""

import json
import re
import sys
from datetime import datetime

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%Y/%m/%d",
    "%Y%m%d%H%M%S",
    "%Y%m%d",
]

DISPLAY_FMT = "%Y-%m-%d %H:%M:%S"
ICON_PATH = "icon.png"


def item(title, subtitle="", copy_value=None, arg=None, valid=True):
    value = arg if arg is not None else copy_value
    if value is None:
        value = title
    row = {
        "uid": f"{title}-{subtitle}",
        "type": "default",
        "title": title,
        "subtitle": subtitle,
        "arg": str(value),
        "icon": {"path": ICON_PATH},
    }
    if valid:
        row["valid"] = True
    else:
        row["valid"] = False
    return row


def emit(items):
    print(json.dumps({"items": items}, ensure_ascii=False))


def parse_datetime(text):
    text = text.strip()
    if not text:
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def from_unix_seconds(seconds):
    return datetime.fromtimestamp(seconds)


def from_unix_millis(ms):
    return datetime.fromtimestamp(ms / 1000.0)


def format_dt(dt):
    return dt.strftime(DISPLAY_FMT)


def handle_now():
    now = datetime.now()
    sec = int(now.timestamp())
    ms = sec * 1000
    compact = now.strftime("%Y%m%d%H%M%S")
    return [
        item(
            str(sec),
            f"Unix 秒 · {format_dt(now)}",
            copy_value=sec,
        ),
        item(
            str(ms),
            f"Unix 毫秒 · {format_dt(now)}",
            copy_value=ms,
        ),
        item(
            compact,
            f"紧凑时间 · {format_dt(now)}",
            copy_value=compact,
        ),
        item(
            format_dt(now),
            "本地时间",
            copy_value=format_dt(now),
        ),
    ]


def handle_date(text):
    dt = parse_datetime(text)
    if dt is None:
        return [
                item(
                    "无法解析日期",
                    "支持: 2025-01-01、2025-01-01 12:30:00、2025/01/01",
                    arg="",
                    valid=False,
                )
        ]
    sec = int(dt.timestamp())
    return [
        item(
            str(sec),
            f"Unix 秒 · {format_dt(dt)}",
            copy_value=sec,
        ),
        item(
            str(sec * 1000),
            f"Unix 毫秒 · {format_dt(dt)}",
            copy_value=sec * 1000,
        ),
    ]


def handle_unix_seconds(text):
    sec = int(text)
    dt = from_unix_seconds(sec)
    formatted = format_dt(dt)
    return [
        item(
            formatted,
            f"Unix 秒 {sec}",
            copy_value=formatted,
        ),
        item(
            str(sec * 1000),
            "对应毫秒时间戳",
            copy_value=sec * 1000,
        ),
    ]


def handle_unix_millis(text):
    ms = int(text)
    dt = from_unix_millis(ms)
    formatted = format_dt(dt)
    sec = ms // 1000
    return [
        item(
            formatted,
            f"Unix 毫秒 {ms}",
            copy_value=formatted,
        ),
        item(
            str(sec),
            "对应秒级时间戳",
            copy_value=sec,
        ),
    ]


def handle_help(query):
    hint = "now | 2025-01-01 | 1779357292 | 1779357292000"
    if query:
        hint = f"输入: {query}"
    return [
        item("time now", "当前 Unix 秒 / 毫秒 / 20260526111213 / 本地时间", arg="now", valid=False),
        item("time 2025-01-01", "日期 → 10 位 Unix 秒", arg="2025-01-01", valid=False),
        item("time 1779357292", "10 位 Unix 秒 → 日期时间", arg="1779357292", valid=False),
        item(
            "time 1779357292000",
            "13 位 Unix 毫秒 → 日期时间",
            arg="1779357292000",
            valid=False,
        ),
        item("用法", hint, arg="", valid=False),
    ]


def main():
    query = (sys.argv[1] if len(sys.argv) > 1 else "").strip()

    if not query or query.lower() == "now":
        emit(handle_now() if query else handle_help("") + handle_now())
        return

    if re.fullmatch(r"\d{10}", query):
        emit(handle_unix_seconds(query))
        return

    if re.fullmatch(r"\d{13}", query):
        emit(handle_unix_millis(query))
        return

    if re.fullmatch(r"\d{11,12}", query):
        emit(
            [
                item(
                    "位数异常",
                    "秒级用 10 位，毫秒用 13 位",
                    arg="",
                    valid=False,
                )
            ]
        )
        return

    dt = parse_datetime(query)
    if dt is not None:
        emit(handle_date(query))
        return

    emit(handle_help(query))


if __name__ == "__main__":
    main()
