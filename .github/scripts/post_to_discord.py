"""Post journal entries to the Discord #recaps channel.

Usage: python post_to_discord.py _posts/2026-11-17-some-title.md [...]
Needs the DISCORD_WEBHOOK environment variable (a GitHub secret).
Posts a short summary card that links to the entry's own page on the site.
"""
import datetime
import json
import os
import re
import sys
import urllib.request

SITE = "https://awizzlebased.github.io/awintrades"
SAGE = 0xA3B19B
SUMMARY_MAX = 350


def parse(path):
    text = open(path, encoding="utf-8").read()
    meta, body = {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("'\"")
        body = m.group(2)
    return meta, body


def clean(md):
    md = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", md)  # linked images
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)               # images
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)            # links -> text
    md = re.sub(r"\{\{.*?\}\}|\{%.*?%\}", "", md)               # liquid
    md = re.sub(r"[*_`]", "", md)
    return md.strip()


def summary(body):
    # first paragraph under "What happened", else the first paragraph of the entry
    sec = re.search(r"^#+\s*What happened\s*$(.*?)(?=^#+\s|\Z)", body, re.S | re.M | re.I)
    chunk = sec.group(1) if sec else re.sub(r"^#+.*$", "", body, flags=re.M)
    paras = [clean(p) for p in re.split(r"\n\s*\n", chunk)]
    paras = [p for p in paras if p]
    s = " ".join(paras[0].split()) if paras else ""
    if len(s) > SUMMARY_MAX:
        s = s[:SUMMARY_MAX].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    return s


def card(path):
    meta, body = parse(path)
    name = os.path.basename(path)
    day = name[:10]
    date = datetime.date.fromisoformat(day)
    link = f"{SITE}/#journal/{day}"
    status = meta.get("status", "traded").lower().replace("-", " ")

    desc = []
    if meta.get("takeaway"):
        desc.append(f"> **{meta['takeaway']}**")
    s = summary(body)
    if s:
        desc.append(s)
    desc.append(f"[Read the full entry →]({link})")

    fields = [{"name": "Market", "value": meta.get("market", "ES Futures"), "inline": True},
              {"name": "Day", "value": "Sat out" if status == "sat out" else "Traded", "inline": True}]
    if meta.get("setup"):
        fields.append({"name": "Setup", "value": meta["setup"], "inline": True})
    if meta.get("grade"):
        fields.append({"name": "Process grade", "value": meta["grade"], "inline": True})

    embed = {
        "author": {"name": f"Trading Journal · {date.strftime('%a, %b')} {date.day}, {date.year}"},
        "title": meta.get("title", name[11:-3].replace("-", " ").capitalize()),
        "url": link,
        "description": "\n\n".join(desc),
        "color": SAGE,
        "fields": fields,
        "footer": {"text": "Awin Trades · Education only, not financial advice"},
    }
    img = re.search(r"/assets/journal/[^)\s\"']+\.(?:png|jpe?g|gif|webp)", body, re.I)
    if img:
        embed["image"] = {"url": SITE + img.group(0)}
    return embed


def send(embed):
    data = json.dumps({"username": "Awin Trades", "embeds": [embed],
                       "allowed_mentions": {"parse": []}}).encode()
    req = urllib.request.Request(
        os.environ["DISCORD_WEBHOOK"], data=data, method="POST",
        headers={"Content-Type": "application/json",
                 "User-Agent": "AwinTradesJournal (https://awizzlebased.github.io/awintrades, 1.0)"})
    with urllib.request.urlopen(req) as r:
        print("posted", embed["title"], r.status)


if __name__ == "__main__":
    if not os.environ.get("DISCORD_WEBHOOK"):
        sys.exit("DISCORD_WEBHOOK secret is not set")
    for p in sys.argv[1:]:
        e = card(p)
        if os.environ.get("DRY_RUN"):
            print(json.dumps(e, indent=2, ensure_ascii=False))
        else:
            send(e)
