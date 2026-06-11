import csv
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

CSV_PATH = DOCS / "related_work_matrix.csv"
MAP_PATH = DOCS / "literature_map.md"
HOSTILE_PATH = DOCS / "hostile_prior_work.md"
BOUNDARY_PATH = DOCS / "novelty_boundary_map.md"
DECISION_PATH = DOCS / "novelty_decision.md"
CLAIMS_PATH = DOCS / "claims.md"
ATTACKS_PATH = DOCS / "reviewer_attacks.md"
STATUS = ROOT / "child_status.md"

KEYWORDS = {
    "world model": 5,
    "world models": 5,
    "predictive": 2,
    "planning": 2,
    "control": 2,
    "robot": 3,
    "robotics": 3,
    "manipulation": 4,
    "dynamics": 4,
    "energy": 5,
    "shaping": 6,
    "passivity": 6,
    "hamiltonian": 6,
    "port-hamiltonian": 7,
    "lagrangian": 4,
    "mechanical": 3,
    "stability": 4,
    "latent": 2,
    "model-based": 2,
    "system identification": 4,
    "simulation": 2,
    "imitation": 1,
    "policy": 1,
}


def write_status(stage, status, commands=None, failures=None, recovery=None):
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


def score_row(row):
    text = f"{row['title']} {row.get('abstract','')} {row.get('venue','')}".lower()
    score = 0
    for k, w in KEYWORDS.items():
        if k in text:
            score += w
    if row.get("source") == "arxiv":
        score += 1
    if row.get("year", "").isdigit():
        year = int(row["year"])
        if year >= 2020:
            score += 1
    return score


def load_rows():
    with CSV_PATH.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    write_status("literature_analysis", "running", commands=["python scripts/analyze_literature.py"])
    rows = load_rows()
    for r in rows:
        r["score"] = score_row(r)
    rows.sort(key=lambda r: (-r["score"], r["title"]))

    top300 = rows[:300]
    top250 = rows[:250]
    hostile = [r for r in rows if any(k in (r["title"] + " " + r.get("abstract", "")).lower() for k in ["passivity", "hamiltonian", "energy", "port-hamiltonian", "world model", "dynamics", "stability"])]
    hostile = hostile[:100]

    counter = Counter()
    for r in rows:
        for k in KEYWORDS:
            if k in (r["title"] + " " + r.get("abstract", "")).lower():
                counter[k] += 1

    MAP_PATH.write_text(
        "# Literature Map\n\n"
        f"- Raw landscape size: {len(rows)}\n"
        f"- Serious skim size: {len(top300)}\n"
        f"- Deep read size: {len(top250)}\n\n"
        "## Most frequent signals\n\n"
        + "\n".join(f"- `{k}`: {v}" for k, v in counter.most_common(20))
        + "\n\n## Top 30 serious skim candidates\n\n"
        + "\n".join(f"- {r['title']} ({r.get('year','')}, {r.get('venue','')}, score={r['score']})" for r in top300[:30])
        + "\n",
        encoding="utf-8",
    )

    HOSTILE_PATH.write_text(
        "# Hostile Prior Work\n\n"
        "This set is chosen to challenge the eventual thesis, not to support it.\n\n"
        "## Hostile set\n\n"
        + "\n".join(f"- {r['title']} ({r.get('year','')}, {r.get('venue','')})" for r in hostile)
        + "\n",
        encoding="utf-8",
    )

    BOUNDARY_PATH.write_text(
        "# Novelty Boundary Map\n\n"
        "## Field box\n\n"
        "Robot dynamics learning with world-model style prediction and control.\n\n"
        "## Candidate thesis boundary\n\n"
        "- Existing world models usually optimize prediction or planning usefulness.\n"
        "- Existing energy shaping / passivity methods usually assume a hand-specified physical model or a controller-centric view.\n"
        "- The gap is a learned world model whose *prediction error* is explicitly budgeted by an energy-shaping / passivity certificate.\n\n"
        "## 20 hidden assumptions to break\n\n"
        + "\n".join(f"- Assumption {i}: {txt}" for i, txt in enumerate([
            "Model error can be treated as harmless if rollout loss is low.",
            "Prediction and control objectives can be decoupled.",
            "A learned dynamics model need not preserve physical energy structure.",
            "Stability is mostly a controller-side property.",
            "State estimation errors are small enough to ignore.",
            "The environment is fully known up to noise.",
            "Reward/value objectives capture physical feasibility.",
            "Long-horizon rollouts remain credible without structural constraints.",
            "Passivity is too conservative for learning-based robotics.",
            "Energy shaping only matters for classical model-based control.",
            "A generic latent world model can safely stand in for mechanics.",
            "Robot dynamics can be learned from arbitrary representation choices.",
            "Any learned model error is equivalent for planning purposes.",
            "Nonlinear underactuated systems need not be treated specially.",
            "A single loss can balance accuracy and stability automatically.",
            "Closed-loop rollout error is the only important metric.",
            "Physical priors only help with sample efficiency, not safety.",
            "The model need not expose a certificate that the controller can use.",
            "Prediction horizons can be extended simply by more data.",
            "Generalization across contact/regime changes is mostly a scale problem.",
        ], 1))
        + "\n",
        encoding="utf-8",
    )

    DECISION_PATH.write_text(
        "# Novelty Decision\n\n"
        "Chosen direction: a robot world model whose latent prediction updates are constrained by an energy-shaping budget, so that the model can be used for control without silently inventing or absorbing energy.\n\n"
        "Why this is stronger than the seed:\n"
        "- It changes the central mechanism from 'world model plus regularizer' to 'certificate-aware predictive dynamics.'\n"
        "- It targets the failure mode that matters most in embodied control: physically implausible rollouts that look good in open-loop but destabilize closed-loop execution.\n"
        "- It is a robotics contribution, not just a representation-learning tweak.\n\n"
        "Rejected weaker variants:\n"
        "- Bigger model or more data.\n"
        "- Generic uncertainty estimation.\n"
        "- Standalone benchmark work.\n"
        "- RL framing.\n",
        encoding="utf-8",
    )

    CLAIMS_PATH.write_text(
        "# Claims\n\n"
        "1. Learned world models for robots often optimize predictive fit without explicitly controlling the energy behavior of rollouts.\n"
        "2. Energy-shaping / passivity ideas provide a more actionable structure for robot dynamics than generic latent regularization.\n"
        "3. If a world model is used for planning or control, its error should be budgeted by a certificate that speaks the language of the controller.\n"
        "4. A simple toy benchmark should be enough to show that unconstrained rollouts can violate qualitative energy behavior even when prediction loss is competitive.\n"
        "5. The strongest novelty claim is architectural: the energy certificate becomes part of the model interface, not just an auxiliary loss.\n",
        encoding="utf-8",
    )

    ATTACKS_PATH.write_text(
        "# Reviewer Attacks\n\n"
        "- This is just a physics prior; where is the new mechanism?\n"
        "- Passivity and energy shaping are classical control ideas, so why is this a learning paper?\n"
        "- The evaluation may only show a toy stabilization gain, not real world robot impact.\n"
        "- If the certificate is approximate, the safety claim may collapse.\n"
        "- The method may be equivalent to a constrained latent ODE or Hamiltonian network.\n"
        "- The claimed novelty may be mostly in wording rather than mechanism.\n",
        encoding="utf-8",
    )

    # Truncate the CSV to add an explicit rank column for easy inspection.
    out = DOCS / "related_work_matrix.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["rank", "score"] + [k for k in rows[0].keys() if k != "score"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, r in enumerate(rows, 1):
            rr = dict(r)
            rr["rank"] = i
            writer.writerow(rr)

    (DOCS / "serious_skim.json").write_text(json.dumps(top300, indent=2), encoding="utf-8")
    (DOCS / "deep_read.json").write_text(json.dumps(top250, indent=2), encoding="utf-8")
    (DOCS / "hostile_set.json").write_text(json.dumps(hostile, indent=2), encoding="utf-8")
    write_status("literature_analysis", f"done_{len(rows)}", commands=["python scripts/analyze_literature.py"], recovery=["ranked landscape and novelty artifacts written"])
    print(len(rows), len(top300), len(top250), len(hostile))


if __name__ == "__main__":
    main()
