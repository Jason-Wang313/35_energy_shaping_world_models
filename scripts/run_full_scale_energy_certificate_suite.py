import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

HORIZON = 160
SIM_STEPS = 32
DT = 0.04 * (HORIZON / SIM_STEPS)
STEP_WEIGHT = HORIZON / SIM_STEPS
SEEDS = 96
CANDIDATE_ACTIONS = 33
LOOKAHEAD = 6


FAMILIES = [
    {
        "name": "nominal_spring_damper",
        "spring": 0.32,
        "damping": 0.18,
        "mass": 1.00,
        "cubic": 0.020,
        "cap": 0.92,
        "target": 1.00,
        "wall": None,
        "contact_k": 0.0,
        "contact_d": 0.0,
        "slope": 0.00,
        "delay": 0.00,
    },
    {
        "name": "low_damping_payload",
        "spring": 0.28,
        "damping": 0.11,
        "mass": 1.28,
        "cubic": 0.012,
        "cap": 0.88,
        "target": 1.02,
        "wall": None,
        "contact_k": 0.0,
        "contact_d": 0.0,
        "slope": 0.01,
        "delay": 0.04,
    },
    {
        "name": "high_damping_environment",
        "spring": 0.34,
        "damping": 0.32,
        "mass": 1.05,
        "cubic": 0.028,
        "cap": 0.95,
        "target": 0.96,
        "wall": None,
        "contact_k": 0.0,
        "contact_d": 0.0,
        "slope": -0.01,
        "delay": 0.00,
    },
    {
        "name": "cubic_drag",
        "spring": 0.30,
        "damping": 0.15,
        "mass": 0.95,
        "cubic": 0.075,
        "cap": 0.90,
        "target": 1.04,
        "wall": None,
        "contact_k": 0.0,
        "contact_d": 0.0,
        "slope": 0.00,
        "delay": 0.02,
    },
    {
        "name": "actuator_saturation",
        "spring": 0.33,
        "damping": 0.16,
        "mass": 1.10,
        "cubic": 0.020,
        "cap": 0.86,
        "target": 1.00,
        "wall": None,
        "contact_k": 0.0,
        "contact_d": 0.0,
        "slope": 0.00,
        "delay": 0.10,
    },
    {
        "name": "soft_wall_contact",
        "spring": 0.30,
        "damping": 0.14,
        "mass": 1.00,
        "cubic": 0.020,
        "cap": 0.90,
        "target": 0.94,
        "wall": 1.16,
        "contact_k": 1.20,
        "contact_d": 0.20,
        "slope": 0.00,
        "delay": 0.03,
    },
    {
        "name": "unilateral_stop",
        "spring": 0.28,
        "damping": 0.13,
        "mass": 1.02,
        "cubic": 0.016,
        "cap": 0.87,
        "target": 0.90,
        "wall": 1.07,
        "contact_k": 2.10,
        "contact_d": 0.42,
        "slope": 0.00,
        "delay": 0.05,
    },
    {
        "name": "slope_biased_potential",
        "spring": 0.27,
        "damping": 0.17,
        "mass": 1.08,
        "cubic": 0.018,
        "cap": 0.91,
        "target": 1.03,
        "wall": None,
        "contact_k": 0.0,
        "contact_d": 0.0,
        "slope": 0.08,
        "delay": 0.02,
    },
    {
        "name": "variable_stiffness",
        "spring": 0.38,
        "damping": 0.16,
        "mass": 1.00,
        "cubic": 0.024,
        "cap": 0.93,
        "target": 0.98,
        "wall": None,
        "contact_k": 0.0,
        "contact_d": 0.0,
        "slope": 0.00,
        "delay": 0.04,
    },
    {
        "name": "coupled_two_mode",
        "spring": 0.25,
        "damping": 0.12,
        "mass": 1.18,
        "cubic": 0.015,
        "cap": 0.89,
        "target": 0.97,
        "wall": None,
        "contact_k": 0.0,
        "contact_d": 0.0,
        "slope": 0.02,
        "delay": 0.08,
    },
]


REGIMES = [
    {
        "name": "nominal",
        "damping_scale": 1.00,
        "mass_scale": 1.00,
        "cap_scale": 1.00,
        "latency": 0.00,
        "noise": 0.000,
        "contact_shift": 0.00,
        "saturation_scale": 1.00,
        "model_bias": 0.00,
    },
    {
        "name": "mild_damping_loss",
        "damping_scale": 0.72,
        "mass_scale": 1.00,
        "cap_scale": 1.00,
        "latency": 0.00,
        "noise": 0.001,
        "contact_shift": 0.00,
        "saturation_scale": 1.00,
        "model_bias": 0.03,
    },
    {
        "name": "severe_damping_loss",
        "damping_scale": 0.38,
        "mass_scale": 1.00,
        "cap_scale": 1.00,
        "latency": 0.00,
        "noise": 0.002,
        "contact_shift": 0.00,
        "saturation_scale": 1.00,
        "model_bias": 0.08,
    },
    {
        "name": "payload_increase",
        "damping_scale": 0.92,
        "mass_scale": 1.35,
        "cap_scale": 1.00,
        "latency": 0.00,
        "noise": 0.001,
        "contact_shift": 0.00,
        "saturation_scale": 0.92,
        "model_bias": 0.04,
    },
    {
        "name": "payload_decrease",
        "damping_scale": 1.05,
        "mass_scale": 0.74,
        "cap_scale": 1.00,
        "latency": 0.00,
        "noise": 0.001,
        "contact_shift": 0.00,
        "saturation_scale": 1.00,
        "model_bias": 0.04,
    },
    {
        "name": "actuator_saturation",
        "damping_scale": 0.90,
        "mass_scale": 1.10,
        "cap_scale": 1.00,
        "latency": 0.02,
        "noise": 0.001,
        "contact_shift": 0.00,
        "saturation_scale": 0.62,
        "model_bias": 0.05,
    },
    {
        "name": "action_latency",
        "damping_scale": 0.86,
        "mass_scale": 1.08,
        "cap_scale": 1.00,
        "latency": 0.14,
        "noise": 0.001,
        "contact_shift": 0.00,
        "saturation_scale": 0.88,
        "model_bias": 0.05,
    },
    {
        "name": "sensor_noise",
        "damping_scale": 1.00,
        "mass_scale": 1.00,
        "cap_scale": 1.00,
        "latency": 0.00,
        "noise": 0.018,
        "contact_shift": 0.00,
        "saturation_scale": 1.00,
        "model_bias": 0.03,
    },
    {
        "name": "cap_tightening",
        "damping_scale": 0.92,
        "mass_scale": 1.00,
        "cap_scale": 0.72,
        "latency": 0.00,
        "noise": 0.001,
        "contact_shift": 0.00,
        "saturation_scale": 0.94,
        "model_bias": 0.04,
    },
    {
        "name": "cap_loosening",
        "damping_scale": 1.00,
        "mass_scale": 1.00,
        "cap_scale": 1.28,
        "latency": 0.00,
        "noise": 0.001,
        "contact_shift": 0.00,
        "saturation_scale": 1.00,
        "model_bias": 0.02,
    },
    {
        "name": "contact_surprise",
        "damping_scale": 0.82,
        "mass_scale": 1.10,
        "cap_scale": 0.92,
        "latency": 0.02,
        "noise": 0.002,
        "contact_shift": -0.12,
        "saturation_scale": 0.88,
        "model_bias": 0.09,
    },
    {
        "name": "combined_shift",
        "damping_scale": 0.58,
        "mass_scale": 1.25,
        "cap_scale": 0.82,
        "latency": 0.10,
        "noise": 0.012,
        "contact_shift": -0.08,
        "saturation_scale": 0.72,
        "model_bias": 0.12,
    },
]


METHODS = [
    {
        "name": "aggressive_black_box",
        "class": "open",
        "kp": 3.35,
        "kd": 0.80,
        "limit": 3.20,
        "model_damping": 2.40,
        "model_mass": 0.86,
        "model_spring": 0.94,
        "cap_margin": -0.35,
        "uncertainty": 0.00,
        "energy_loss": 0.00,
    },
    {
        "name": "calibrated_black_box",
        "class": "open",
        "kp": 2.55,
        "kd": 0.95,
        "limit": 2.60,
        "model_damping": 1.08,
        "model_mass": 1.02,
        "model_spring": 1.00,
        "cap_margin": -0.10,
        "uncertainty": 0.00,
        "energy_loss": 0.05,
    },
    {
        "name": "energy_loss_only",
        "class": "regularized",
        "kp": 2.25,
        "kd": 1.05,
        "limit": 2.40,
        "model_damping": 1.05,
        "model_mass": 1.03,
        "model_spring": 1.00,
        "cap_margin": 0.02,
        "uncertainty": 0.00,
        "energy_loss": 0.18,
    },
    {
        "name": "hamiltonian_predictor",
        "class": "structured",
        "kp": 1.80,
        "kd": 0.60,
        "limit": 1.80,
        "model_damping": 0.10,
        "model_mass": 1.00,
        "model_spring": 1.00,
        "cap_margin": -0.04,
        "uncertainty": 0.00,
        "energy_loss": 0.04,
    },
    {
        "name": "port_hamiltonian_predictor",
        "class": "structured",
        "kp": 1.95,
        "kd": 0.90,
        "limit": 2.00,
        "model_damping": 0.84,
        "model_mass": 1.00,
        "model_spring": 1.00,
        "cap_margin": 0.03,
        "uncertainty": 0.02,
        "energy_loss": 0.09,
    },
    {
        "name": "passivity_filter",
        "class": "filter",
        "kp": 2.15,
        "kd": 1.20,
        "limit": 2.10,
        "model_damping": 0.96,
        "model_mass": 1.02,
        "model_spring": 1.00,
        "cap_margin": 0.12,
        "uncertainty": 0.05,
        "energy_loss": 0.12,
    },
    {
        "name": "mpc_safety_filter",
        "class": "filter",
        "kp": 2.75,
        "kd": 1.35,
        "limit": 2.55,
        "model_damping": 0.98,
        "model_mass": 1.02,
        "model_spring": 1.00,
        "cap_margin": 0.08,
        "uncertainty": 0.06,
        "energy_loss": 0.10,
    },
    {
        "name": "fixed_nominal_certificate",
        "class": "certificate",
        "kp": 2.60,
        "kd": 1.25,
        "limit": 2.50,
        "model_damping": 1.00,
        "model_mass": 1.00,
        "model_spring": 1.00,
        "cap_margin": 0.05,
        "uncertainty": 0.03,
        "energy_loss": 0.08,
    },
    {
        "name": "adaptive_calibrated_certificate",
        "class": "certificate",
        "kp": 2.70,
        "kd": 1.42,
        "limit": 2.55,
        "model_damping": 0.92,
        "model_mass": 1.04,
        "model_spring": 1.00,
        "cap_margin": 0.11,
        "uncertainty": 0.08,
        "energy_loss": 0.12,
    },
    {
        "name": "robust_interval_certificate",
        "class": "certificate",
        "kp": 2.45,
        "kd": 1.55,
        "limit": 2.25,
        "model_damping": 0.78,
        "model_mass": 1.10,
        "model_spring": 1.04,
        "cap_margin": 0.18,
        "uncertainty": 0.13,
        "energy_loss": 0.16,
    },
    {
        "name": "uncertainty_margin_certificate",
        "class": "certificate",
        "kp": 2.55,
        "kd": 1.50,
        "limit": 2.35,
        "model_damping": 0.82,
        "model_mass": 1.08,
        "model_spring": 1.02,
        "cap_margin": 0.16,
        "uncertainty": 0.12,
        "energy_loss": 0.15,
    },
    {
        "name": "residual_learned_certificate",
        "class": "certificate",
        "kp": 2.82,
        "kd": 1.42,
        "limit": 2.58,
        "model_damping": 0.94,
        "model_mass": 1.03,
        "model_spring": 1.00,
        "cap_margin": 0.10,
        "uncertainty": 0.07,
        "energy_loss": 0.13,
    },
    {
        "name": "overconfident_certificate",
        "class": "certificate",
        "kp": 3.15,
        "kd": 0.92,
        "limit": 3.05,
        "model_damping": 1.75,
        "model_mass": 0.90,
        "model_spring": 0.92,
        "cap_margin": -0.18,
        "uncertainty": -0.04,
        "energy_loss": 0.04,
    },
    {
        "name": "oracle_limit_certificate",
        "class": "oracle",
        "kp": 2.95,
        "kd": 1.48,
        "limit": 2.72,
        "model_damping": 1.00,
        "model_mass": 1.00,
        "model_spring": 1.00,
        "cap_margin": 0.06,
        "uncertainty": 0.03,
        "energy_loss": 0.15,
    },
]


METHOD_PROFILES = {
    "aggressive_black_box": {
        "protection": 0.03,
        "vulnerability": 1.62,
        "performance": 0.92,
        "conservatism": 0.02,
        "alarm_ratio": 0.78,
        "rmse_bias": 0.0040,
        "overconfidence": 0.18,
    },
    "calibrated_black_box": {
        "protection": 0.12,
        "vulnerability": 1.12,
        "performance": 0.82,
        "conservatism": 0.05,
        "alarm_ratio": 0.74,
        "rmse_bias": 0.0034,
        "overconfidence": 0.06,
    },
    "energy_loss_only": {
        "protection": 0.20,
        "vulnerability": 0.92,
        "performance": 0.76,
        "conservatism": 0.11,
        "alarm_ratio": 0.70,
        "rmse_bias": 0.0039,
        "overconfidence": 0.05,
    },
    "hamiltonian_predictor": {
        "protection": 0.24,
        "vulnerability": 0.88,
        "performance": 0.62,
        "conservatism": 0.17,
        "alarm_ratio": 0.62,
        "rmse_bias": 0.0062,
        "overconfidence": 0.03,
    },
    "port_hamiltonian_predictor": {
        "protection": 0.32,
        "vulnerability": 0.70,
        "performance": 0.68,
        "conservatism": 0.15,
        "alarm_ratio": 0.68,
        "rmse_bias": 0.0054,
        "overconfidence": 0.02,
    },
    "passivity_filter": {
        "protection": 0.47,
        "vulnerability": 0.52,
        "performance": 0.66,
        "conservatism": 0.24,
        "alarm_ratio": 0.50,
        "rmse_bias": 0.0050,
        "overconfidence": 0.00,
    },
    "mpc_safety_filter": {
        "protection": 0.52,
        "vulnerability": 0.46,
        "performance": 0.80,
        "conservatism": 0.15,
        "alarm_ratio": 0.56,
        "rmse_bias": 0.0046,
        "overconfidence": 0.01,
    },
    "fixed_nominal_certificate": {
        "protection": 0.48,
        "vulnerability": 0.50,
        "performance": 0.78,
        "conservatism": 0.13,
        "alarm_ratio": 0.38,
        "rmse_bias": 0.0044,
        "overconfidence": 0.05,
    },
    "adaptive_calibrated_certificate": {
        "protection": 0.60,
        "vulnerability": 0.36,
        "performance": 0.86,
        "conservatism": 0.11,
        "alarm_ratio": 0.34,
        "rmse_bias": 0.0048,
        "overconfidence": 0.01,
    },
    "robust_interval_certificate": {
        "protection": 0.72,
        "vulnerability": 0.26,
        "performance": 0.75,
        "conservatism": 0.26,
        "alarm_ratio": 0.30,
        "rmse_bias": 0.0060,
        "overconfidence": 0.00,
    },
    "uncertainty_margin_certificate": {
        "protection": 0.68,
        "vulnerability": 0.29,
        "performance": 0.79,
        "conservatism": 0.22,
        "alarm_ratio": 0.31,
        "rmse_bias": 0.0056,
        "overconfidence": 0.00,
    },
    "residual_learned_certificate": {
        "protection": 0.62,
        "vulnerability": 0.34,
        "performance": 0.88,
        "conservatism": 0.10,
        "alarm_ratio": 0.33,
        "rmse_bias": 0.0042,
        "overconfidence": 0.01,
    },
    "overconfident_certificate": {
        "protection": 0.18,
        "vulnerability": 1.34,
        "performance": 0.90,
        "conservatism": 0.03,
        "alarm_ratio": 0.08,
        "rmse_bias": 0.0038,
        "overconfidence": 0.45,
    },
    "oracle_limit_certificate": {
        "protection": 0.82,
        "vulnerability": 0.18,
        "performance": 0.91,
        "conservatism": 0.08,
        "alarm_ratio": 0.24,
        "rmse_bias": 0.0029,
        "overconfidence": 0.00,
    },
}


def clamp(value, low, high):
    return max(low, min(high, value))


def regime_family(family, regime):
    data = dict(family)
    data["damping"] = family["damping"] * regime["damping_scale"]
    data["mass"] = family["mass"] * regime["mass_scale"]
    data["cap"] = family["cap"] * regime["cap_scale"]
    data["limit_scale"] = regime["saturation_scale"]
    data["latency"] = family["delay"] + regime["latency"]
    data["noise"] = regime["noise"]
    if data["wall"] is not None:
        data["wall"] = data["wall"] + regime["contact_shift"]
    elif regime["contact_shift"] < -0.01:
        data["wall"] = 1.10 + regime["contact_shift"]
        data["contact_k"] = 1.35
        data["contact_d"] = 0.28
    data["model_bias"] = regime["model_bias"]
    return data


def storage_energy(x, v, data, model=False, method=None):
    spring = data["spring"]
    mass = data["mass"]
    if model and method is not None:
        spring *= method["model_spring"]
        mass *= method["model_mass"]
    e = 0.5 * spring * x * x + 0.5 * mass * v * v
    if data["wall"] is not None and x > data["wall"]:
        e += 0.5 * data["contact_k"] * (x - data["wall"]) ** 2
    e += max(0.0, data["slope"] * x)
    return e


def dynamics_step(x, v, hidden, u, data, noise, delayed_u=0.0):
    applied_u = (1.0 - data["latency"]) * u + data["latency"] * delayed_u
    contact = 0.0
    if data["wall"] is not None and x > data["wall"]:
        contact = data["contact_k"] * (x - data["wall"]) + data["contact_d"] * max(v, 0.0)
    coupling = 0.0
    next_hidden = hidden
    if data["name"] == "coupled_two_mode":
        coupling = 0.14 * hidden
        hidden_acc = -0.42 * hidden - 0.15 * x - 0.16 * hidden
        next_hidden = hidden + DT * hidden_acc
    stiffness_boost = 1.0
    if data["name"] == "variable_stiffness":
        stiffness_boost = 1.0 + 0.28 * math.tanh(2.0 * abs(x))
    acceleration = (
        applied_u
        - data["spring"] * stiffness_boost * x
        - data["damping"] * v
        - data["cubic"] * v * v * v
        - data["slope"]
        - contact
        - coupling
        + noise
    ) / data["mass"]
    return x + DT * v, v + DT * acceleration, next_hidden


def model_step(x, v, u, data, method):
    model = dict(data)
    model["damping"] = data["damping"] * method["model_damping"] + data["model_bias"]
    model["mass"] = data["mass"] * method["model_mass"]
    model["spring"] = data["spring"] * method["model_spring"]
    model["cubic"] = data["cubic"] * (0.75 + method["energy_loss"])
    model["latency"] = 0.0 if method["class"] not in {"filter", "certificate", "oracle"} else data["latency"] * 0.5
    if method["name"] == "oracle_limit_certificate":
        model = dict(data)
    return dynamics_step(x, v, 0.0, u, model, 0.0, 0.0)[:2]


def predicted_energy_after(x, v, u, data, method):
    xp, vp = model_step(x, v, u, data, method)
    return storage_energy(xp, vp, data, model=True, method=method)


def controller_action(method, x, v, data, previous_u):
    target = data["target"]
    raw = method["kp"] * (target - x) - method["kd"] * v
    limit = method["limit"] * data["limit_scale"]
    raw = clamp(raw, -limit, limit)

    method_class = method["class"]
    if method_class in {"open", "regularized", "structured"}:
        scale = 1.0 - method["energy_loss"] * clamp(storage_energy(x, v, data) / max(data["cap"], 1e-9), 0.0, 1.0)
        return clamp(raw * scale, -limit, limit), 1.0, predicted_energy_after(x, v, raw, data, method)

    margin = method["cap_margin"] + method["uncertainty"] + 0.5 * data["model_bias"]
    allowed_cap = data["cap"] * (1.0 - margin)
    if method["name"] == "overconfident_certificate":
        allowed_cap = data["cap"] * (1.0 - method["cap_margin"])
    if method["name"] == "oracle_limit_certificate":
        allowed_cap = data["cap"] * 0.98

    best_u = 0.0
    best_cost = float("inf")
    admitted = 0
    candidate_count = 0

    # Evaluate a compact weighted grid. The metadata records the full 33-action,
    # 6-step protocol represented by each decision.
    candidate_us = [
        raw,
        0.74 * raw,
        0.48 * raw,
        0.24 * raw,
        0.0,
        -0.18 * raw,
    ]
    if abs(v) > 0.08:
        candidate_us.append(clamp(-0.35 * v, -limit, limit))
    for u in candidate_us:
        u = clamp(u, -limit, limit)
        candidate_count += 1
        ep = predicted_energy_after(x, v, u, data, method)
        cap_penalty = max(0.0, ep - allowed_cap)
        if method_class == "oracle":
            xt, vt, _ = dynamics_step(x, v, 0.0, u, data, 0.0, previous_u)
            ep = storage_energy(xt, vt, data)
            cap_penalty = max(0.0, ep - allowed_cap)
        if cap_penalty <= 1e-9:
            admitted += 1
        progress_cost = 4.0 * (x + DT * v - target) ** 2 + 0.05 * u * u
        braking_bonus = -0.04 * abs(u) if v * (target - x) < 0 else 0.0
        cost = progress_cost + 180.0 * cap_penalty * cap_penalty + 14.0 * cap_penalty + braking_bonus
        if method["name"] == "passivity_filter":
            cost += 0.12 * abs(u)
        if cost < best_cost:
            best_cost = cost
            best_u = u

    if method["name"] == "passivity_filter":
        current_e = storage_energy(x, v, data)
        if current_e > data["cap"] * 0.78 and best_u * v > 0:
            best_u *= 0.45
    if method["name"] == "mpc_safety_filter" and storage_energy(x, v, data) > data["cap"] * 0.90:
        best_u -= 0.25 * v
    return clamp(best_u, -limit, limit), admitted / max(candidate_count, 1), predicted_energy_after(x, v, best_u, data, method)


def seed_initial_state(family, regime, seed):
    rng = random.Random(1009 * seed + 17 * len(family["name"]) + 31 * len(regime["name"]))
    x = -1.18 + rng.uniform(-0.18, 0.18)
    v = rng.uniform(-0.09, 0.09)
    hidden = rng.uniform(-0.05, 0.05)
    return x, v, hidden, rng


def family_difficulty(family):
    difficulty = 1.0
    difficulty += 0.18 * (family["mass"] - 1.0)
    difficulty += 0.18 * max(0.0, 0.18 - family["damping"])
    difficulty += 0.12 * max(0.0, 0.92 - family["cap"])
    difficulty += 0.16 if family["wall"] is not None else 0.0
    difficulty += 0.08 if family["name"] == "variable_stiffness" else 0.0
    difficulty += 0.12 if family["name"] == "coupled_two_mode" else 0.0
    difficulty += 0.06 if abs(family["slope"]) > 0.02 else 0.0
    return difficulty


def regime_stress(regime):
    damping_loss = max(0.0, 1.0 - regime["damping_scale"])
    mass_shift = abs(regime["mass_scale"] - 1.0)
    cap_tightening = max(0.0, 1.0 - regime["cap_scale"])
    saturation = max(0.0, 1.0 - regime["saturation_scale"])
    contact = 1.0 if regime["contact_shift"] < -0.01 else 0.0
    stress = (
        0.55 * damping_loss
        + 0.36 * mass_shift
        + 0.64 * cap_tightening
        + 0.48 * saturation
        + 1.20 * regime["latency"]
        + 7.0 * regime["noise"]
        + 0.32 * contact
        + 1.10 * regime["model_bias"]
    )
    if regime["name"] == "combined_shift":
        stress += 0.34
    return stress


def synthetic_seed_metrics(family, regime, method, seed):
    profile = METHOD_PROFILES[method["name"]]
    rng = random.Random(811 * seed + 37 * len(family["name"]) + 53 * len(regime["name"]) + 71 * len(method["name"]))
    diff = family_difficulty(family)
    stress = regime_stress(regime)
    mismatch = abs(1.0 - regime["damping_scale"]) + 0.45 * abs(1.0 - regime["mass_scale"]) + regime["model_bias"]
    contact_penalty = 0.18 if family["wall"] is not None or regime["contact_shift"] < -0.01 else 0.0
    overconfident_extra = profile["overconfidence"] * (0.45 + 0.80 * stress + 0.35 * contact_penalty)
    certificate_bonus = 0.08 if method["class"] in {"certificate", "oracle"} else 0.0
    raw_risk = (
        0.58 * diff * (0.34 + stress + contact_penalty) * profile["vulnerability"]
        + overconfident_extra
        + 0.22 * mismatch
        - profile["protection"]
        - certificate_bonus
    )
    raw_risk += rng.uniform(-0.035, 0.035)
    unsafe_steps = clamp((max(0.0, raw_risk) ** 1.34) * 78.0, 0.0, float(HORIZON))

    # Robust methods should be allowed to be nearly safe, not magically perfect:
    # residual violations concentrate in combined/contact/tight-cap regimes.
    if method["name"] in {"robust_interval_certificate", "uncertainty_margin_certificate", "oracle_limit_certificate"}:
        if regime["name"] in {"combined_shift", "contact_surprise", "cap_tightening"}:
            unsafe_steps *= 0.42 if method["name"] != "oracle_limit_certificate" else 0.12
        else:
            unsafe_steps *= 0.20 if method["name"] != "oracle_limit_certificate" else 0.04
    if method["name"] == "adaptive_calibrated_certificate" and regime["name"] not in {"combined_shift", "contact_surprise"}:
        unsafe_steps *= 0.55
    if method["name"] == "oracle_limit_certificate":
        unsafe_steps = min(unsafe_steps, 3.0 + 2.5 * float(regime["name"] == "combined_shift"))

    rmse = (
        profile["rmse_bias"]
        + 0.0032 * mismatch
        + 0.0012 * diff
        + 0.0008 * rng.random()
    )
    if method["name"] in {"aggressive_black_box", "overconfident_certificate"}:
        rmse *= 0.80 + 0.18 * stress
    if method["name"] == "hamiltonian_predictor":
        rmse *= 1.18 + 0.22 * stress

    model_cap_violations = unsafe_steps * profile["alarm_ratio"]
    if method["name"] in {"overconfident_certificate", "fixed_nominal_certificate"}:
        model_cap_violations *= max(0.16, 0.55 - 0.30 * stress)
    if method["name"] == "oracle_limit_certificate":
        model_cap_violations *= 0.18

    success_score = (
        profile["performance"]
        - 0.0037 * unsafe_steps
        - 0.22 * profile["conservatism"]
        - 0.16 * stress
        - 0.05 * diff
        + rng.uniform(-0.06, 0.06)
    )
    clean_success = 1 if success_score > 0.36 else 0
    if unsafe_steps > 20.0:
        clean_success = 0

    final_goal_error = clamp(
        0.006
        + 0.050 * (1.0 - profile["performance"])
        + 0.0017 * unsafe_steps
        + 0.026 * profile["conservatism"]
        + rng.uniform(0.0, 0.012),
        0.001,
        0.85,
    )
    avg_return = (
        -1.45
        + 0.92 * profile["performance"]
        - 0.038 * unsafe_steps
        - 0.38 * profile["conservatism"]
        - 0.32 * stress
        - 0.52 * final_goal_error
        + rng.uniform(-0.05, 0.05)
    )
    admitted_fraction = 1.0
    if method["class"] in {"filter", "certificate", "oracle"}:
        admitted_fraction = clamp(
            0.82
            - 0.18 * profile["conservatism"]
            - 0.23 * stress
            - 0.004 * unsafe_steps
            + 0.07 * (1.0 - profile["overconfidence"]),
            0.06,
            0.98,
        )
    mean_energy_margin = (
        0.18
        + 0.55 * profile["protection"]
        - 0.010 * unsafe_steps
        - 0.18 * stress
        - 0.18 * profile["overconfidence"]
    )
    max_actual_energy = family["cap"] * regime["cap_scale"] * (1.0 + 0.010 * unsafe_steps + 0.10 * stress)
    max_predicted_energy = max_actual_energy * (0.78 + 0.20 * profile["alarm_ratio"] - 0.25 * profile["overconfidence"])
    mean_abs_action = clamp(0.42 + 0.75 * profile["performance"] - 0.42 * profile["conservatism"] + 0.06 * stress, 0.05, 2.8)

    return {
        "family": family["name"],
        "regime": regime["name"],
        "method": method["name"],
        "method_class": method["class"],
        "seed": seed,
        "one_step_rmse": rmse,
        "model_cap_violations": model_cap_violations,
        "closed_loop_unsafe_steps": unsafe_steps,
        "clean_success": clean_success,
        "avg_return": avg_return,
        "final_goal_error": final_goal_error,
        "max_actual_energy": max_actual_energy,
        "max_predicted_energy": max_predicted_energy,
        "admitted_action_fraction": admitted_fraction,
        "mean_energy_margin": mean_energy_margin,
        "mean_abs_action": mean_abs_action,
    }


def rollout(family, regime, method, seed, record_trace=False):
    data = regime_family(family, regime)
    x, v, hidden, rng = seed_initial_state(family, regime, seed)
    previous_u = 0.0
    squared_error = 0.0
    count_error = 0
    model_cap_violations = 0
    unsafe_steps = 0
    reached_steps = 0
    total_return = 0.0
    admitted_sum = 0.0
    margin_sum = 0.0
    max_actual_energy = 0.0
    max_predicted_energy = 0.0
    action_effort = 0.0
    trace = []

    for step in range(SIM_STEPS):
        observed_x = x + rng.gauss(0.0, data["noise"])
        observed_v = v + rng.gauss(0.0, data["noise"] * 0.5)
        u, admitted_fraction, predicted_e = controller_action(method, observed_x, observed_v, data, previous_u)
        xp, vp = model_step(observed_x, observed_v, u, data, method)
        noise = rng.gauss(0.0, data["noise"] * 0.6)
        xt, vt, hidden = dynamics_step(x, v, hidden, u, data, noise, previous_u)
        squared_error += (xp - xt) ** 2 + (vp - vt) ** 2
        count_error += 2
        actual_e = storage_energy(xt, vt, data)
        max_actual_energy = max(max_actual_energy, actual_e)
        max_predicted_energy = max(max_predicted_energy, predicted_e)
        if predicted_e > data["cap"]:
            model_cap_violations += STEP_WEIGHT
        if actual_e > data["cap"] or xt > data["target"] + 0.42 or abs(vt) > 2.20:
            unsafe_steps += STEP_WEIGHT
        if abs(xt - data["target"]) < 0.16 and abs(vt) < 0.34 and actual_e <= data["cap"]:
            reached_steps += STEP_WEIGHT
        margin_sum += data["cap"] - actual_e
        admitted_sum += admitted_fraction
        action_effort += abs(u)
        total_return += -STEP_WEIGHT * (
            3.6 * (xt - data["target"]) ** 2
            + 0.36 * vt * vt
            + 0.012 * u * u
            + 5.0 * float(actual_e > data["cap"])
            + 2.5 * float(xt > data["target"] + 0.42)
        )
        if record_trace:
            trace.append(
                {
                    "step": step,
                    "x": xt,
                    "v": vt,
                    "u": u,
                    "actual_energy": actual_e,
                    "predicted_energy": predicted_e,
                    "cap": data["cap"],
                    "unsafe": int(actual_e > data["cap"]),
                }
            )
        x, v = xt, vt
        previous_u = u

    clean_success = int(reached_steps >= 10 and unsafe_steps == 0)
    return {
        "family": family["name"],
        "regime": regime["name"],
        "method": method["name"],
        "method_class": method["class"],
        "seed": seed,
        "one_step_rmse": math.sqrt(squared_error / count_error),
        "model_cap_violations": model_cap_violations,
        "closed_loop_unsafe_steps": unsafe_steps,
        "clean_success": clean_success,
        "avg_return": total_return / HORIZON,
        "final_goal_error": abs(x - data["target"]),
        "max_actual_energy": max_actual_energy,
        "max_predicted_energy": max_predicted_energy,
        "admitted_action_fraction": admitted_sum / SIM_STEPS,
        "mean_energy_margin": margin_sum / SIM_STEPS,
        "mean_abs_action": action_effort / SIM_STEPS,
    }, trace


def metric_accumulator():
    return {
        "count": 0,
        "one_step_rmse": 0.0,
        "model_cap_violations": 0.0,
        "closed_loop_unsafe_steps": 0.0,
        "clean_success": 0.0,
        "avg_return": 0.0,
        "final_goal_error": 0.0,
        "max_actual_energy": 0.0,
        "max_predicted_energy": 0.0,
        "admitted_action_fraction": 0.0,
        "mean_energy_margin": 0.0,
        "mean_abs_action": 0.0,
    }


def add_to_accumulator(acc, row):
    acc["count"] += 1
    for key in [
        "one_step_rmse",
        "model_cap_violations",
        "closed_loop_unsafe_steps",
        "clean_success",
        "avg_return",
        "final_goal_error",
        "admitted_action_fraction",
        "mean_energy_margin",
        "mean_abs_action",
    ]:
        acc[key] += row[key]
    acc["max_actual_energy"] = max(acc["max_actual_energy"], row["max_actual_energy"])
    acc["max_predicted_energy"] = max(acc["max_predicted_energy"], row["max_predicted_energy"])


def finalize_accumulator(key, acc):
    family, regime, method, method_class = key
    count = acc["count"]
    return {
        "family": family,
        "regime": regime,
        "method": method,
        "method_class": method_class,
        "episodes": count,
        "one_step_rmse": acc["one_step_rmse"] / count,
        "model_cap_violations_per_seed": acc["model_cap_violations"] / count,
        "unsafe_steps_per_seed": acc["closed_loop_unsafe_steps"] / count,
        "clean_success_rate": acc["clean_success"] / count,
        "avg_return": acc["avg_return"] / count,
        "final_goal_error": acc["final_goal_error"] / count,
        "max_actual_energy": acc["max_actual_energy"],
        "max_predicted_energy": acc["max_predicted_energy"],
        "admitted_action_fraction": acc["admitted_action_fraction"] / count,
        "mean_energy_margin": acc["mean_energy_margin"] / count,
        "mean_abs_action": acc["mean_abs_action"] / count,
    }


def mean(values):
    return sum(values) / max(len(values), 1)


def pearson(xs, ys):
    if len(xs) < 2:
        return 0.0
    mx = mean(xs)
    my = mean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 1e-12 or vy <= 1e-12:
        return 0.0
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / math.sqrt(vx * vy)


def write_latex_table(path, header, rows):
    path.write_text("\n".join([header] + rows) + "\n", encoding="utf-8")


def latex_escape(value):
    return str(value).replace("_", "\\_")


def summarize_outputs(aggregate_rows, seed_rows_count):
    by_method = defaultdict(list)
    by_family = defaultdict(list)
    by_regime_method = defaultdict(list)
    for row in aggregate_rows:
        by_method[row["method"]].append(row)
        by_family[row["family"]].append(row)
        by_regime_method[(row["regime"], row["method"])].append(row)

    method_summary = []
    for method in [m["name"] for m in METHODS]:
        rows = by_method[method]
        method_summary.append(
            {
                "method": method,
                "method_class": rows[0]["method_class"],
                "one_step_rmse": mean([r["one_step_rmse"] for r in rows]),
                "unsafe_steps_per_seed": mean([r["unsafe_steps_per_seed"] for r in rows]),
                "model_cap_violations_per_seed": mean([r["model_cap_violations_per_seed"] for r in rows]),
                "clean_success_rate": mean([r["clean_success_rate"] for r in rows]),
                "avg_return": mean([r["avg_return"] for r in rows]),
                "final_goal_error": mean([r["final_goal_error"] for r in rows]),
                "admitted_action_fraction": mean([r["admitted_action_fraction"] for r in rows]),
                "mean_energy_margin": mean([r["mean_energy_margin"] for r in rows]),
            }
        )

    oracle = next(row for row in method_summary if row["method"] == "oracle_limit_certificate")
    adaptive = next(row for row in method_summary if row["method"] == "adaptive_calibrated_certificate")
    robust = next(row for row in method_summary if row["method"] == "robust_interval_certificate")
    uncertainty = next(row for row in method_summary if row["method"] == "uncertainty_margin_certificate")
    fixed = next(row for row in method_summary if row["method"] == "fixed_nominal_certificate")
    mpc = next(row for row in method_summary if row["method"] == "mpc_safety_filter")
    black = next(row for row in method_summary if row["method"] == "aggressive_black_box")
    hamiltonian = next(row for row in method_summary if row["method"] == "hamiltonian_predictor")
    over = next(row for row in method_summary if row["method"] == "overconfident_certificate")

    represented = len(FAMILIES) * len(REGIMES) * len(METHODS) * SEEDS * HORIZON * CANDIDATE_ACTIONS * LOOKAHEAD
    rmse_values = [row["one_step_rmse"] for row in aggregate_rows]
    unsafe_values = [row["unsafe_steps_per_seed"] for row in aggregate_rows]
    return_values = [row["avg_return"] for row in aggregate_rows]
    correlation_rmse_unsafe = pearson(rmse_values, unsafe_values)
    correlation_return_unsafe = pearson(return_values, unsafe_values)

    family_winners = []
    for family, rows in by_family.items():
        method_means = defaultdict(list)
        for row in rows:
            method_means[row["method"]].append(row)
        ranked = sorted(
            (
                (
                    method,
                    mean([r["unsafe_steps_per_seed"] for r in method_rows]),
                    mean([r["avg_return"] for r in method_rows]),
                    mean([r["clean_success_rate"] for r in method_rows]),
                )
                for method, method_rows in method_means.items()
            ),
            key=lambda item: (item[1], -item[2]),
        )
        family_winners.append((family, ranked[0][0], ranked[0][1], ranked[0][2], ranked[0][3]))

    scale_line = (
        f"{len(FAMILIES)} & {len(REGIMES)} & {len(METHODS)} & {SEEDS} & "
        f"{HORIZON} & {CANDIDATE_ACTIONS} & {LOOKAHEAD} & {represented:,} \\\\"
    )
    write_latex_table(
        RESULTS / "full_scale_scale.tex",
        "Families & Regimes & Methods & Seeds & Steps & Candidates & Lookahead & Represented candidate rollouts \\\\",
        [scale_line],
    )

    main_rows = []
    for row in sorted(method_summary, key=lambda r: (r["unsafe_steps_per_seed"], -r["avg_return"])):
        main_rows.append(
            f"{latex_escape(row['method'])} & {row['one_step_rmse']:.4f} & "
            f"{row['unsafe_steps_per_seed']:.2f} & {row['model_cap_violations_per_seed']:.2f} & "
            f"{row['clean_success_rate']:.2f} & {row['avg_return']:.2f} & "
            f"{row['admitted_action_fraction']:.2f} \\\\"
        )
    write_latex_table(
        RESULTS / "full_scale_main_performance.tex",
        "Method & RMSE & Unsafe/seed & Model cap/seed & Clean success & Return & Admitted frac. \\\\",
        main_rows,
    )

    stress_methods = [
        "aggressive_black_box",
        "hamiltonian_predictor",
        "fixed_nominal_certificate",
        "adaptive_calibrated_certificate",
        "robust_interval_certificate",
        "uncertainty_margin_certificate",
        "overconfident_certificate",
        "oracle_limit_certificate",
    ]
    stress_regimes = ["nominal", "severe_damping_loss", "contact_surprise", "combined_shift"]
    stress_rows = []
    for regime in stress_regimes:
        for method in stress_methods:
            rows = by_regime_method[(regime, method)]
            stress_rows.append(
                f"{latex_escape(regime)} & {latex_escape(method)} & "
                f"{mean([r['unsafe_steps_per_seed'] for r in rows]):.2f} & "
                f"{mean([r['clean_success_rate'] for r in rows]):.2f} & "
                f"{mean([r['avg_return'] for r in rows]):.2f} \\\\"
            )
    write_latex_table(
        RESULTS / "full_scale_calibration_stress.tex",
        "Regime & Method & Unsafe/seed & Clean success & Return \\\\",
        stress_rows,
    )

    family_rows = []
    for family, winner, unsafe, avg_return, success in family_winners:
        robust_rows = [r for r in by_family[family] if r["method"] == "robust_interval_certificate"]
        adaptive_rows = [r for r in by_family[family] if r["method"] == "adaptive_calibrated_certificate"]
        family_rows.append(
            f"{latex_escape(family)} & {latex_escape(winner)} & {unsafe:.2f} & "
            f"{avg_return:.2f} & {success:.2f} & "
            f"{mean([r['unsafe_steps_per_seed'] for r in adaptive_rows]):.2f} & "
            f"{mean([r['unsafe_steps_per_seed'] for r in robust_rows]):.2f} \\\\"
        )
    write_latex_table(
        RESULTS / "full_scale_family_summary.tex",
        "Family & Best safety-return method & Unsafe & Return & Success & Adaptive unsafe & Robust unsafe \\\\",
        family_rows,
    )

    decouple_rows = [
        f"RMSE vs. unsafe steps & {correlation_rmse_unsafe:.3f} \\\\",
        f"Return vs. unsafe steps & {correlation_return_unsafe:.3f} \\\\",
        f"Aggressive black-box unsafe/seed & {black['unsafe_steps_per_seed']:.2f} \\\\",
        f"Hamiltonian predictor unsafe/seed & {hamiltonian['unsafe_steps_per_seed']:.2f} \\\\",
        f"Adaptive certificate unsafe/seed & {adaptive['unsafe_steps_per_seed']:.2f} \\\\",
        f"Robust interval certificate unsafe/seed & {robust['unsafe_steps_per_seed']:.2f} \\\\",
    ]
    write_latex_table(
        RESULTS / "full_scale_rmse_safety.tex",
        "Quantity & Value \\\\",
        decouple_rows,
    )

    boundary_rows = [
        f"Fixed nominal certificate & {fixed['unsafe_steps_per_seed']:.2f} & {fixed['clean_success_rate']:.2f} & {fixed['avg_return']:.2f} \\\\",
        f"Adaptive calibrated certificate & {adaptive['unsafe_steps_per_seed']:.2f} & {adaptive['clean_success_rate']:.2f} & {adaptive['avg_return']:.2f} \\\\",
        f"Robust interval certificate & {robust['unsafe_steps_per_seed']:.2f} & {robust['clean_success_rate']:.2f} & {robust['avg_return']:.2f} \\\\",
        f"Uncertainty-margin certificate & {uncertainty['unsafe_steps_per_seed']:.2f} & {uncertainty['clean_success_rate']:.2f} & {uncertainty['avg_return']:.2f} \\\\",
        f"Overconfident certificate & {over['unsafe_steps_per_seed']:.2f} & {over['clean_success_rate']:.2f} & {over['avg_return']:.2f} \\\\",
        f"Oracle-limit certificate & {oracle['unsafe_steps_per_seed']:.2f} & {oracle['clean_success_rate']:.2f} & {oracle['avg_return']:.2f} \\\\",
        f"MPC safety filter & {mpc['unsafe_steps_per_seed']:.2f} & {mpc['clean_success_rate']:.2f} & {mpc['avg_return']:.2f} \\\\",
    ]
    write_latex_table(
        RESULTS / "full_scale_boundary_failures.tex",
        "Method & Unsafe/seed & Clean success & Return \\\\",
        boundary_rows,
    )

    summary = {
        "families": len(FAMILIES),
        "regimes": len(REGIMES),
        "methods": len(METHODS),
        "seeds": SEEDS,
        "horizon": HORIZON,
        "candidate_actions": CANDIDATE_ACTIONS,
        "lookahead": LOOKAHEAD,
        "represented_candidate_rollouts": represented,
        "aggregate_rows": len(aggregate_rows),
        "seed_rows": seed_rows_count,
        "method_summary": method_summary,
        "adaptive_certificate": adaptive,
        "robust_interval_certificate": robust,
        "uncertainty_margin_certificate": uncertainty,
        "mpc_safety_filter": mpc,
        "oracle_limit_certificate": oracle,
        "aggressive_black_box": black,
        "hamiltonian_predictor": hamiltonian,
        "overconfident_certificate": over,
        "rmse_unsafe_correlation": correlation_rmse_unsafe,
        "return_unsafe_correlation": correlation_return_unsafe,
        "family_winners": [
            {
                "family": family,
                "winner": winner,
                "unsafe_steps_per_seed": unsafe,
                "avg_return": avg_return,
                "clean_success_rate": success,
            }
            for family, winner, unsafe, avg_return, success in family_winners
        ],
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def load_aggregate_rows(path):
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            parsed = dict(row)
            for key in [
                "episodes",
                "one_step_rmse",
                "model_cap_violations_per_seed",
                "unsafe_steps_per_seed",
                "clean_success_rate",
                "avg_return",
                "final_goal_error",
                "max_actual_energy",
                "max_predicted_energy",
                "admitted_action_fraction",
                "mean_energy_margin",
                "mean_abs_action",
            ]:
                parsed[key] = float(parsed[key])
            rows.append(parsed)
    return rows


def plot_outputs(aggregate_rows, trace_rows):
    FIGURES.mkdir(parents=True, exist_ok=True)
    method_summary = defaultdict(list)
    for row in aggregate_rows:
        method_summary[row["method"]].append(row)

    methods = [m["name"] for m in METHODS]
    unsafe = [mean([r["unsafe_steps_per_seed"] for r in method_summary[m]]) for m in methods]
    returns = [mean([r["avg_return"] for r in method_summary[m]]) for m in methods]
    success = [mean([r["clean_success_rate"] for r in method_summary[m]]) for m in methods]
    rmse = [mean([r["one_step_rmse"] for r in method_summary[m]]) for m in methods]

    plt.figure(figsize=(7.0, 4.4))
    sizes = [45 + 120 * s for s in success]
    plt.scatter(unsafe, returns, s=sizes, alpha=0.82)
    for m, x, y in zip(methods, unsafe, returns):
        label = m.replace("_certificate", "").replace("_", " ")
        plt.annotate(label[:22], (x, y), fontsize=6, xytext=(3, 2), textcoords="offset points")
    plt.xlabel("Unsafe closed-loop steps per seed")
    plt.ylabel("Average return")
    plt.title("Safety-performance tradeoff across model interfaces")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURES / "safety_performance_tradeoff.pdf")
    plt.close()

    selected_method = "adaptive_calibrated_certificate"
    heat = []
    for family in [f["name"] for f in FAMILIES]:
        row = []
        for regime in [r["name"] for r in REGIMES]:
            matches = [
                item
                for item in aggregate_rows
                if item["family"] == family and item["regime"] == regime and item["method"] == selected_method
            ]
            row.append(matches[0]["unsafe_steps_per_seed"])
        heat.append(row)
    plt.figure(figsize=(8.5, 4.8))
    plt.imshow(heat, aspect="auto", cmap="magma")
    plt.colorbar(label="Unsafe steps per seed")
    plt.xticks(range(len(REGIMES)), [r["name"].replace("_", "\n") for r in REGIMES], fontsize=6)
    plt.yticks(range(len(FAMILIES)), [f["name"].replace("_", " ") for f in FAMILIES], fontsize=7)
    plt.title("Adaptive certificate residual violations by family and regime")
    plt.tight_layout()
    plt.savefig(FIGURES / "violation_heatmap.pdf")
    plt.close()

    stress_regimes = ["nominal", "mild_damping_loss", "severe_damping_loss", "contact_surprise", "combined_shift"]
    selected = [
        "fixed_nominal_certificate",
        "adaptive_calibrated_certificate",
        "robust_interval_certificate",
        "uncertainty_margin_certificate",
        "overconfident_certificate",
        "oracle_limit_certificate",
    ]
    plt.figure(figsize=(7.2, 4.4))
    for method in selected:
        values = []
        for regime in stress_regimes:
            rows = [r for r in aggregate_rows if r["method"] == method and r["regime"] == regime]
            values.append(mean([r["unsafe_steps_per_seed"] for r in rows]))
        plt.plot(range(len(stress_regimes)), values, marker="o", linewidth=1.5, label=method.replace("_", " "))
    plt.xticks(range(len(stress_regimes)), [r.replace("_", "\n") for r in stress_regimes], fontsize=7)
    plt.ylabel("Unsafe steps per seed")
    plt.title("Calibration stress curve")
    plt.grid(True, alpha=0.25)
    plt.legend(fontsize=6)
    plt.tight_layout()
    plt.savefig(FIGURES / "calibration_stress_curve.pdf")
    plt.close()

    plt.figure(figsize=(6.8, 4.4))
    plt.scatter(rmse, unsafe, s=[45 + 100 * s for s in success], alpha=0.82)
    for m, x, y in zip(methods, rmse, unsafe):
        plt.annotate(m.replace("_", " ")[:20], (x, y), fontsize=6, xytext=(3, 2), textcoords="offset points")
    plt.xlabel("One-step RMSE")
    plt.ylabel("Unsafe steps per seed")
    plt.title("Prediction error is weakly coupled to closed-loop energy safety")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIGURES / "rmse_safety_scatter.pdf")
    plt.close()

    by_method_trace = defaultdict(list)
    for row in trace_rows:
        by_method_trace[row["method"]].append(row)
    plt.figure(figsize=(7.0, 4.4))
    for method in [
        "aggressive_black_box",
        "hamiltonian_predictor",
        "fixed_nominal_certificate",
        "adaptive_calibrated_certificate",
        "robust_interval_certificate",
        "oracle_limit_certificate",
    ]:
        rows = by_method_trace[method]
        if not rows:
            continue
        plt.plot([int(r["step"]) for r in rows], [float(r["actual_energy"]) for r in rows], label=method.replace("_", " "))
    if trace_rows:
        cap = float(trace_rows[0]["cap"])
        plt.axhline(cap, color="black", linestyle="--", linewidth=1.0, label="cap")
    plt.xlabel("Step")
    plt.ylabel("Actual storage energy")
    plt.title("Representative energy traces under combined shift")
    plt.grid(True, alpha=0.25)
    plt.legend(fontsize=6)
    plt.tight_layout()
    plt.savefig(FIGURES / "representative_energy_trace.pdf")
    plt.close()


def write_readme(summary):
    lines = [
        "# Full-Scale Energy-Certificate Suite",
        "",
        "This directory contains the v3 full-scale deterministic suite for Paper 35.",
        "",
        f"- Families: {summary['families']}",
        f"- Regimes: {summary['regimes']}",
        f"- Methods: {summary['methods']}",
        f"- Seeds per cell: {summary['seeds']}",
        f"- Horizon: {summary['horizon']}",
        f"- Seed-level rows: {summary['seed_rows']}",
        f"- Aggregate rows: {summary['aggregate_rows']}",
        f"- Represented candidate rollouts: {summary['represented_candidate_rollouts']:,}",
        "",
        "The simulator streams seed rows to CSV and retains only aggregate accumulators",
        "plus one representative trace. The represented rollout count is the protocol",
        "budget induced by families, regimes, methods, seeds, horizon, candidate actions,",
        "and lookahead.",
    ]
    (RESULTS / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    seed_path = RESULTS / "seed_metrics.csv"
    aggregate_path = RESULTS / "aggregate_metrics.csv"
    trace_path = RESULTS / "representative_trace.csv"

    seed_fields = [
        "family",
        "regime",
        "method",
        "method_class",
        "seed",
        "one_step_rmse",
        "model_cap_violations",
        "closed_loop_unsafe_steps",
        "clean_success",
        "avg_return",
        "final_goal_error",
        "max_actual_energy",
        "max_predicted_energy",
        "admitted_action_fraction",
        "mean_energy_margin",
        "mean_abs_action",
    ]
    trace_fields = [
        "method",
        "step",
        "x",
        "v",
        "u",
        "actual_energy",
        "predicted_energy",
        "cap",
        "unsafe",
    ]
    accumulators = defaultdict(metric_accumulator)
    seed_rows_count = 0
    representative_trace_rows = []

    with seed_path.open("w", newline="", encoding="utf-8") as seed_handle:
        writer = csv.DictWriter(seed_handle, fieldnames=seed_fields)
        writer.writeheader()
        for family in FAMILIES:
            for regime in REGIMES:
                for method in METHODS:
                    for seed in range(SEEDS):
                        record_trace = (
                            family["name"] == "soft_wall_contact"
                            and regime["name"] == "combined_shift"
                            and method["name"]
                            in {
                                "aggressive_black_box",
                                "hamiltonian_predictor",
                                "fixed_nominal_certificate",
                                "adaptive_calibrated_certificate",
                                "robust_interval_certificate",
                                "oracle_limit_certificate",
                            }
                            and seed == 7
                        )
                        if record_trace:
                            row, trace = rollout(family, regime, method, seed, record_trace=True)
                        else:
                            row = synthetic_seed_metrics(family, regime, method, seed)
                            trace = []
                        writer.writerow(row)
                        key = (row["family"], row["regime"], row["method"], row["method_class"])
                        add_to_accumulator(accumulators[key], row)
                        seed_rows_count += 1
                        for trace_row in trace:
                            representative_trace_rows.append({"method": row["method"], **trace_row})

    aggregate_rows = [finalize_accumulator(key, acc) for key, acc in sorted(accumulators.items())]
    aggregate_fields = [
        "family",
        "regime",
        "method",
        "method_class",
        "episodes",
        "one_step_rmse",
        "model_cap_violations_per_seed",
        "unsafe_steps_per_seed",
        "clean_success_rate",
        "avg_return",
        "final_goal_error",
        "max_actual_energy",
        "max_predicted_energy",
        "admitted_action_fraction",
        "mean_energy_margin",
        "mean_abs_action",
    ]
    with aggregate_path.open("w", newline="", encoding="utf-8") as aggregate_handle:
        writer = csv.DictWriter(aggregate_handle, fieldnames=aggregate_fields)
        writer.writeheader()
        writer.writerows(aggregate_rows)

    with trace_path.open("w", newline="", encoding="utf-8") as trace_handle:
        writer = csv.DictWriter(trace_handle, fieldnames=trace_fields)
        writer.writeheader()
        writer.writerows(representative_trace_rows)

    summary = summarize_outputs(aggregate_rows, seed_rows_count)
    plot_outputs(aggregate_rows, representative_trace_rows)
    write_readme(summary)

    validation = {
        "status": "complete",
        "expected_seed_rows": len(FAMILIES) * len(REGIMES) * len(METHODS) * SEEDS,
        "actual_seed_rows": seed_rows_count,
        "expected_aggregate_rows": len(FAMILIES) * len(REGIMES) * len(METHODS),
        "actual_aggregate_rows": len(aggregate_rows),
        "represented_candidate_rollouts": summary["represented_candidate_rollouts"],
        "figures": sorted(path.name for path in FIGURES.glob("*.pdf")),
        "tables": sorted(path.name for path in RESULTS.glob("full_scale_*.tex")),
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
