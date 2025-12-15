import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import feedparser
import requests

# Official IPA RSS feeds
FEEDS: List[str] = [
    # CHANGED: Only important security alerts (no general news)
    "https://www.ipa.go.jp/security/alert-rss.rdf",  # Important security alerts
]

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

STATE_PATH = Path("sent.json")
MAX_POST_PER_RUN = int(os.environ.get("MAX_POST_PER_RUN", "20"))
HTTP_TIMEOUT_SEC = int(os.environ.get("HTTP_TIMEOUT_SEC", "20"))


def load_sent() -> Set[str]:
    if not STATE_PATH.exists():
        return set()
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return set(str(x) for x in data)
    except Exception:
        pass
    return set()


def save_sent(sent: Set[str]) -> None:
    # Keep recent items only to avoid unbounded growth
    trimmed = list(sent)[-5000:]
    STATE_PATH.write_text(json.dumps(trimmed, ensure_ascii=False, indent=2), encoding="utf-8")


def entry_key(e: Dict[str, Any]) -> str:
    # Prefer a stable key: link -> id -> title fallback
    return str(e.get("link") or e.get("id") or (e.get("title", "") + "|" + str(e)))


def post_to_discord(content: str) -> None:
    payload = {
        "content": content,
        # Avoid accidental @everyone/@here mentions
        "allowed_mentions": {"parse": []},
    }

    r = requests.post(WEBHOOK_URL, json=payload, timeout=HTTP_TIMEOUT_SEC)

    # Basic 429 handling: respect Retry-After header
    if r.status_code == 429:
        retry_after = float(r.headers.get("Retry-After", "5"))
        time.sleep(retry_after)
        r = requests.post(WEBHOOK_URL, json=payload, timeout=HTTP_TIMEOUT_SEC)

    r.raise_for_status()


def sort_key(e: Dict[str, Any]) -> Any:
    # feedparser returns time structs in *_parsed fields
    return e.get("published_parsed") or e.get("updated_parsed") or 0


def main() -> None:
    sent = load_sent()

    new_items: List[Tuple[str, Dict[str, Any]]] = []
    for feed_url in FEEDS:
        d = feedparser.parse(feed_url)
        for e in d.entries:
            k = entry_key(e)
            if k in sent:
                continue
            new_items.append((k, e))

    new_items.sort(key=lambda t: sort_key(t[1]))

    posted = 0
    for k, e in new_items:
        if posted >= MAX_POST_PER_RUN:
            break
        title = e.get("title", "(no title)")
        link = e.get("link", "")
        msg = f"**{title}**\n{link}"
        post_to_discord(msg)
        sent.add(k)
        posted += 1

    save_sent(sent)
    print(f"posted={posted} total_sent={len(sent)}")


if __name__ == "__main__":
    main()
