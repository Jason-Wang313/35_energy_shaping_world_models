import csv
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DT = 0.05
SPRING = 0.30
DAMPING_TRUE = 0.18
TARGET = 1.00
ENERGY_CAP = 0.90
EPISODES = 60
HORIZON_STEPS = 120


def energy(x, v):
    return 0.5 * SPRING * x * x + 0.5 * v * v


def clip(value, low, high):
    return max(low, min(high, value))


def true_step(x, v, u):
    acceleration = u - SPRING * x - DAMPING_TRUE * v - 0.04 * v * v * v
    return x + DT * v, v + DT * acceleration


def model_step(method, x, v, u):
    if method == "black_box":
        acceleration = u - SPRING * x - 0.65 * v - 0.15 * math.tanh(v)
    elif method == "hamiltonian":
        acceleration = u - SPRING * x
    elif method == "certificate":
        acceleration = u - SPRING * x - DAMPING_TRUE * v - 0.02 * math.tanh(v)
    else:
        raise ValueError(method)
    return x + DT * v, v + DT * acceleration


def choose_action(method, x, v):
    if method == "black_box":
        return clip(3.2 * (TARGET - x) - 1.0 * v, -3.0, 3.0)
    if method == "hamiltonian":
        return clip(0.9 * (TARGET - x) - 0.5 * v, -1.0, 1.0)

    desired = clip(3.2 * (TARGET - x) - 1.3 * v, -3.0, 3.0)
    candidates = [desired] + [0.15 * i for i in range(-20, 21)]
    best_cost = float("inf")
    best_u = 0.0
    for u in candidates:
        xp, vp = x, v
        cost = 0.0
        max_energy = 0.0
        for _ in range(6):
            xp, vp = model_step("certificate", xp, vp, u)
            e = energy(xp, vp)
            max_energy = max(max_energy, e)
            cost += 10.0 * (xp - TARGET) ** 2 + 0.4 * vp * vp + 0.005 * u * u
        violation = max(0.0, max_energy - ENERGY_CAP)
        cost += 5000.0 * violation * violation + 300.0 * violation
        if cost < best_cost:
            best_cost = cost
            best_u = u
    return best_u


def rollout(method, seed):
    rnd = random.Random(seed)
    x = -1.2 + rnd.uniform(-0.15, 0.15)
    v = rnd.uniform(-0.05, 0.05)
    squared_error = 0.0
    error_count = 0
    model_energy_cap_violations = 0
    actual_unsafe_steps = 0
    reached_steps = 0
    total_return = 0.0

    for _ in range(HORIZON_STEPS):
        u = choose_action(method, x, v)
        xp, vp = model_step(method, x, v, u)
        xt, vt = true_step(x, v, u)
        squared_error += (xp - xt) ** 2 + (vp - vt) ** 2
        error_count += 2
        if energy(xp, vp) > ENERGY_CAP:
            model_energy_cap_violations += 1
        x, v = xt, vt
        actual_energy = energy(x, v)
        if actual_energy > ENERGY_CAP or x > 1.35 or abs(v) > 1.90:
            actual_unsafe_steps += 1
        if abs(x - TARGET) < 0.18 and abs(v) < 0.30:
            reached_steps += 1
        total_return += -(
            3.0 * (x - TARGET) ** 2
            + 0.3 * v * v
            + 0.015 * u * u
            + 4.0 * float(actual_energy > ENERGY_CAP)
        )

    return {
        "mse": squared_error / error_count,
        "model_energy_cap_violations": model_energy_cap_violations,
        "actual_unsafe_steps": actual_unsafe_steps,
        "clean_success": 1 if reached_steps >= 8 and actual_unsafe_steps == 0 else 0,
        "avg_return": total_return / HORIZON_STEPS,
        "final_goal_error": abs(x - TARGET),
    }


def summarize(method):
    runs = [rollout(method, seed) for seed in range(EPISODES)]
    return {
        "method": method,
        "one_step_rmse": math.sqrt(sum(r["mse"] for r in runs) / len(runs)),
        "model_energy_cap_violations": sum(r["model_energy_cap_violations"] for r in runs),
        "closed_loop_unsafe_steps": sum(r["actual_unsafe_steps"] for r in runs),
        "clean_success_rate": sum(r["clean_success"] for r in runs) / len(runs),
        "avg_return": sum(r["avg_return"] for r in runs) / len(runs),
        "final_goal_error": sum(r["final_goal_error"] for r in runs) / len(runs),
    }


def main():
    rows = [summarize(method) for method in ["black_box", "hamiltonian", "certificate"]]
    DOCS.mkdir(exist_ok=True)
    with (DOCS / "energy_certificate_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
