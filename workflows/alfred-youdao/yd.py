#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alfred Script Filter: Youdao translate (yd keyword)."""

import hashlib
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://openapi.youdao.com/api"
ICON_PATH = "icon.png"

CHINESE_RE = re.compile(
    r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]"
)
WORD_RE = re.compile(r"[A-Za-z']+")
# 常见英文词；纯拉丁但不在词表则视为其它语言（如 bonjour）
EN_WORDS = frozenset(
    """
    a an the is are was were be been being am i you he she it we they me him her us them
    my your his its our their this that these those what which who whom whose
    do does did done have has had can could will would shall should may might must
    not no yes ok okay hello hi hey bye good bad new old big small how why when where
    and or but if so as at by for from in on to of with without about into over
    after before up down out off all any some many much more most very too also just
    get got make made take took go went come came see saw know knew think thought say
    said tell told ask use work play run walk talk read write live love like want need
    help try look find give back here there now then today tomorrow yesterday world
    time day year people man woman child school home life day night water food money
    english chinese translate word sentence
    """.split()
)
ERROR_HINTS = {
    "101": "缺少参数",
    "108": "应用 ID 无效",
    "202": "签名错误，请检查 App Secret",
    "401": "账户欠费",
    "411": "访问频率受限",
}


def emit(items):
    print(json.dumps({"items": items}, ensure_ascii=False))


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
    if valid:
        row["valid"] = True
    else:
        row["valid"] = False
    return row


def load_credentials():
    app_key = os.environ.get("youdao_app_key", "").strip()
    app_secret = os.environ.get("youdao_app_secret", "").strip()
    if app_key and app_secret:
        return app_key, app_secret

    config_path = Path(__file__).resolve().parent / "config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            return (
                str(data.get("app_key", "")).strip(),
                str(data.get("app_secret", "")).strip(),
            )
        except (json.JSONDecodeError, OSError):
            pass
    return "", ""


def truncate(q):
    if len(q) <= 20:
        return q
    return q[:10] + str(len(q)) + q[-10:]


def sign(app_key, app_secret, q, salt, curtime):
    raw = app_key + truncate(q) + salt + str(curtime) + app_secret
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def has_chinese(text):
    return bool(CHINESE_RE.search(text))


def looks_english(text):
    if has_chinese(text):
        return False
    words = [w.lower() for w in WORD_RE.findall(text)]
    if not words:
        return False
    hits = sum(1 for w in words if w in EN_WORDS)
    if len(words) == 1:
        return hits == 1
    return hits >= max(1, int(len(words) * 0.5))


def lang_pair(text):
    """中文→英；英文→中；其它→中。"""
    if has_chinese(text):
        return "zh-CHS", "en", "中文 → 英文"
    if looks_english(text):
        return "en", "zh-CHS", "英文 → 中文"
    return "auto", "zh-CHS", "自动识别 → 中文"


def translate(text, app_key, app_secret):
    from_lang, to_lang, direction = lang_pair(text)
    salt = str(uuid.uuid4())
    curtime = int(time.time())
    payload = {
        "q": text,
        "from": from_lang,
        "to": to_lang,
        "appKey": app_key,
        "salt": salt,
        "sign": sign(app_key, app_secret, text, salt, curtime),
        "signType": "v3",
        "curtime": str(curtime),
    }
    body = urlencode(payload).encode("utf-8")
    req = Request(API_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    code = str(data.get("errorCode", ""))
    if code != "0":
        msg = ERROR_HINTS.get(code, f"有道 API 错误 {code}")
        raise RuntimeError(msg)

    translations = data.get("translation") or []
    if not translations:
        raise RuntimeError("未返回翻译结果")

    result = translations[0]
    meta = data.get("l", f"{from_lang}2{to_lang}")
    return result, direction, meta


def help_items(query=""):
    hint = "你好 | hello | bonjour"
    if query:
        hint = f"正在翻译: {query}"
    return [
        item("yd 你好", "中文 → 英文", arg="你好", valid=False),
        item("yd hello", "英文 → 中文", arg="hello", valid=False),
        item("yd bonjour", "其它语言 → 中文", arg="bonjour", valid=False),
        item("用法", hint, arg="", valid=False),
    ]


def main():
    query = (sys.argv[1] if len(sys.argv) > 1 else "").strip()

    if not query:
        emit(help_items())
        return

    app_key, app_secret = load_credentials()
    if not app_key or not app_secret:
        emit(
            [
                item(
                    "未配置有道 API",
                    "Workflow 变量或 config.json 填写 app_key / app_secret",
                    arg="",
                    valid=False,
                ),
                item(
                    "申请密钥",
                    "https://ai.youdao.com/console/",
                    arg="https://ai.youdao.com/console/",
                    valid=False,
                ),
            ]
        )
        return

    try:
        result, direction, meta = translate(query, app_key, app_secret)
    except (HTTPError, URLError) as exc:
        emit([item("网络错误", str(exc), arg="", valid=False)])
        return
    except RuntimeError as exc:
        emit([item("翻译失败", str(exc), arg="", valid=False)])
        return
    except Exception as exc:
        emit([item("错误", str(exc), arg="", valid=False)])
        return

    emit(
        [
            item(
                result,
                f"{direction} · {meta} · 回车复制",
                arg=result,
            ),
            item(
                query,
                "原文",
                arg=query,
                valid=False,
            ),
        ]
    )


if __name__ == "__main__":
    main()
