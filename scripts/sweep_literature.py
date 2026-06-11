import csv
import json
import re
import sys
import time
from collections import OrderedDict
from pathlib import Path
from xml.etree import ElementTree as ET

import requests


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

OUT_CSV = DOCS / "related_work_matrix.csv"
OUT_JSON = DOCS / "literature_raw.json"
STATUS = ROOT / "child_status.md"

QUERIES = [
    "world model robot dynamics control",
    "robot world models control planning",
    "energy shaping robot control passivity",
    "passivity-based control robot learning",
    "Hamiltonian neural network robot dynamics",
    "neural state space models robotics dynamics",
    "model-based reinforcement learning robotics dynamics",
    "latent dynamics model robot manipulation",
    "predictive control learned dynamics robot",
    "energy-based model robot dynamics learning",
    "port-Hamiltonian learning robot",
    "structured dynamical systems learning robotics",
    "robot dynamics identification learning",
    "learning mechanical systems control robotics",
    "adaptive control robot dynamics learning",
    "model predictive control learned dynamics robotics",
    "system identification robotics dynamics",
    "learning latent dynamics physical systems",
    "neural differential equations control robotics",
    "continuous-time world models robotics",
    "physics-informed dynamics learning robotics",
    "robot manipulation dynamics learning",
    "sim-to-real robot dynamics model learning",
    "embodied world models robot action",
    "predictive state representation robotics",
    "stochastic dynamics learning robot control",
    "energy shaping control learning",
    "passivity robotics reinforcement learning",
]


def write_status(stage: str, status: str, commands=None, failures=None, recovery=None):
    lines = [
        f"stage: {stage}",
        f"status: {status}",
        "commands:",
    ]
    for cmd in commands or []:
        lines.append(f"- {cmd}")
    lines.append("failures:")
    for fail in failures or ["none"]:
        lines.append(f"- {fail}")
    lines.append("recovery:")
    for rec in recovery or ["none yet"]:
        lines.append(f"- {rec}")
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip())


def crossref_query(q, rows=100, cursor="*"):
    url = "https://api.crossref.org/works"
    params = {
        "query": q,
        "rows": rows,
        "cursor": cursor,
        "cursor-max": 1000,
        "mailto": "codex@example.com",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def arxiv_query(q, start=0, max_results=100):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{q}",
        "start": start,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.text


def arxiv_items(q, start=0, max_results=100):
    text = arxiv_query(q, start=start, max_results=max_results)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(text)
    items = []
    for entry in root.findall("a:entry", ns):
        title = norm(entry.findtext("a:title", default="", namespaces=ns))
        if not title:
            continue
        summary = clean_abstract(entry.findtext("a:summary", default="", namespaces=ns))
        published = norm(entry.findtext("a:published", default="", namespaces=ns))
        items.append({
            "title": title,
            "query": q,
            "source": "arxiv",
            "doi": "",
            "url": norm(entry.findtext("a:id", default="", namespaces=ns)),
            "venue": "arXiv",
            "year": published[:4] if published else "",
            "abstract": summary,
            "type": "article",
        })
    return items


def clean_abstract(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return norm(s)


def extract_entries():
    records = OrderedDict()
    raw = {"crossref": [], "arxiv": []}
    for q in QUERIES:
        try:
            data = crossref_query(q, rows=200)
            items = data["message"]["items"]
            for it in items:
                title = norm((it.get("title") or [""])[0])
                if not title:
                    continue
                key = title.lower()
                rec = {
                    "title": title,
                    "query": q,
                    "source": "crossref",
                    "doi": it.get("DOI", ""),
                    "url": it.get("URL", ""),
                    "venue": norm((it.get("container-title") or [""])[0]),
                    "year": str((it.get("issued", {}).get("date-parts", [[None]])[0][0] or "")),
                    "abstract": clean_abstract(it.get("abstract", "")),
                    "type": it.get("type", ""),
                }
                if key not in records:
                    records[key] = rec
            raw["crossref"].append({"query": q, "count": len(items)})
        except Exception as e:
            raw["crossref"].append({"query": q, "error": str(e)})
        time.sleep(0.5)
        try:
            for it in arxiv_items(q, start=0, max_results=100):
                key = it["title"].lower()
                if key not in records:
                    records[key] = it
            raw["arxiv"].append({"query": q, "count": 100})
        except Exception as e:
            raw["arxiv"].append({"query": q, "error": str(e)})
        time.sleep(0.5)
    return list(records.values()), raw


def main():
    write_status("literature_sweep", "running", commands=["python scripts/sweep_literature.py"])
    records, raw = extract_entries()
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "year", "venue", "source", "query", "doi", "url", "type", "abstract"])
        writer.writeheader()
        writer.writerows(records)
    OUT_JSON.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    write_status("literature_sweep", f"done_{len(records)}", commands=["python scripts/sweep_literature.py"], recovery=["crossref harvest completed"])
    print(len(records))


if __name__ == "__main__":
    sys.exit(main())
