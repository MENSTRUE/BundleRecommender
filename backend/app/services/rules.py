"""Read genuine notebook outputs, never fabricate a recommendation.

This adapter accepts CSV rules with antecedents/consequents or comparable
column names. It deliberately fails with actionable errors for unknown schemas.
"""
from __future__ import annotations

import ast
import csv
import json
import math
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.core.config import MODEL_DIR, EXPORT_DIR

DATASETS = ("instacart", "uci")

@dataclass(frozen=True)
class Rule:
    antecedents: tuple[str, ...]
    consequents: tuple[str, ...]
    support: float | None
    confidence: float | None
    lift: float | None


def _field(row: dict[str, str], *aliases: str) -> str | None:
    normalized = {re.sub(r"[^a-z0-9]", "", k.lower()): v for k, v in row.items() if k}
    for alias in aliases:
        value = normalized.get(re.sub(r"[^a-z0-9]", "", alias.lower()))
        if value is not None:
            return value
    return None


def _items(value: str | None) -> tuple[str, ...]:
    if value is None or not value.strip():
        return ()
    raw = value.strip()
    # Common mlxtend CSV representation: frozenset({'item', 'item2'}).
    if raw.startswith("frozenset(") and raw.endswith(")"):
        raw = raw[len("frozenset("):-1]
    parsed = None
    try:
        parsed = json.loads(raw)
    except (ValueError, TypeError):
        try:
            parsed = ast.literal_eval(raw)
        except (ValueError, SyntaxError, TypeError, MemoryError):
            pass
    if isinstance(parsed, (set, list, tuple)):
        pieces = list(parsed)
    elif isinstance(parsed, str):
        pieces = [parsed]
    else:
        # Supports exported strings of the form "item A | item B".
        pieces = re.split(r"\s*[|;,]\s*", raw.strip("{}[]()"))
    cleaned = [str(p).strip().strip("'\"") for p in pieces]
    return tuple(sorted(set(p for p in cleaned if p)))


def _number(value: str | None) -> float | None:
    if value is None or not str(value).strip():
        return None
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except (TypeError, ValueError):
        return None


def artifact(dataset: str) -> Path:
    if dataset not in DATASETS:
        raise ValueError("Unknown dataset; supported: instacart, uci")
    return MODEL_DIR / f"{dataset}_rules.csv"


@lru_cache(maxsize=4)
def _load_cached(path: str, mtime: int, size: int) -> tuple[Rule, ...]:
    rules: list[Rule] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"Rule CSV has no header: {path}")
        headers = [h.strip() for h in reader.fieldnames]
        norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
        h = {norm(v) for v in headers}
        left = {norm(v) for v in ("antecedents", "antecedent", "lhs", "itemsets_a", "if_items")}
        right = {norm(v) for v in ("consequents", "consequent", "rhs", "itemsets_b", "then_items")}
        if not h.intersection(left) or not h.intersection(right):
            raise ValueError(
                f"Unsupported rule columns: {headers}. Expected antecedents/consequents "
                "(or lhs/rhs). Check the notebook export schema before adapting."
            )
        for row in reader:
            a = _items(_field(row, "antecedents", "antecedent", "lhs", "itemsets_a", "if_items"))
            c = _items(_field(row, "consequents", "consequent", "rhs", "itemsets_b", "then_items"))
            if not a or not c or set(a) & set(c):
                continue
            rules.append(Rule(
                antecedents=a,
                consequents=c,
                support=_number(_field(row, "support", "rule_support")),
                confidence=_number(_field(row, "confidence", "rule_confidence")),
                lift=_number(_field(row, "lift")),
            ))
    if not rules:
        raise ValueError(f"No valid association rules in {path}")
    return tuple(rules)


def load_rules(dataset: str) -> tuple[Rule, ...]:
    path = artifact(dataset)
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. Copy notebook exports into models/.")
    stat = path.stat()
    return _load_cached(str(path), stat.st_mtime_ns, stat.st_size)


def catalog(dataset: str) -> list[str]:
    values: set[str] = set()
    for rule in load_rules(dataset):
        values.update(rule.antecedents)
        values.update(rule.consequents)
    return sorted(values, key=str.casefold)


def recommend(dataset: str, items: list[str], limit: int) -> dict:
    rules = load_rules(dataset)
    available = {v.casefold(): v for v in catalog(dataset)}
    requested = list(dict.fromkeys(v.strip() for v in items if v.strip()))
    if not requested:
        raise ValueError("Please select at least one product")
    unknown = [v for v in requested if v.casefold() not in available]
    if unknown:
        raise ValueError(f"Products not found in rule catalog: {unknown[:5]}. Choose from /catalog.")
    selected = {available[v.casefold()] for v in requested}
    selected_casefold = {v.casefold() for v in selected}
    candidates: dict[str, dict] = {}
    matches = 0
    for rule in rules:
        a = {v.casefold() for v in rule.antecedents}
        if not a.issubset(selected_casefold):
            continue
        matches += 1
        for product in rule.consequents:
            if product.casefold() in selected_casefold:
                continue
            score = rule.lift if rule.lift is not None else rule.confidence
            if score is None:
                score = rule.support
            new = dict(product=product, score=score, support=rule.support,
                       confidence=rule.confidence, lift=rule.lift,
                       matched_input=list(rule.antecedents), source=f"{dataset}_rules.csv")
            previous = candidates.get(product.casefold())
            if previous is None or (score or -1) > (previous["score"] or -1):
                candidates[product.casefold()] = new
    ranked = sorted(candidates.values(), key=lambda d: (-(d["score"] or 0), d["product"].casefold()))
    return dict(dataset=dataset, items=sorted(selected), suggestions=ranked[:limit],
                matched_rules=matches, scanned_rules=len(rules),
                disclaimer="Association rules show co-occurrence, not causal effects, purchase probability, or guaranteed sales uplift. Results depend on dataset and rule-mining choices.")


def status() -> dict:
    result = {}
    for name in DATASETS:
        p = artifact(name)
        result[name] = {"available": p.is_file(), "file": str(p.relative_to(MODEL_DIR))}
    return result
