"""Read genuine BundleRecommender notebook association-rule artifacts.

Supported exported schemas:
- Instacart: antecedent_id, consequent_id, antecedent_name, consequent_name
- UCI: antecedent_sku, consequent_sku
- Generic: antecedents, consequents (serialized itemsets)

No fabricated products, metrics, labels, or recommendations are introduced.
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

from app.core.config import MODEL_DIR

DATASETS = ("instacart", "uci")


@dataclass(frozen=True)
class Rule:
    antecedents: tuple[str, ...]
    consequents: tuple[str, ...]
    support: float | None
    confidence: float | None
    lift: float | None


def _key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _field(row: dict[str, str], *aliases: str) -> str | None:
    normalized = {_key(key): value for key, value in row.items() if key}
    for alias in aliases:
        value = normalized.get(_key(alias))
        if value is not None:
            return str(value)
    return None


def _number(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None


def _items(value: str | None) -> tuple[str, ...]:
    """Parse generic CSV itemsets; no eval or code execution."""
    if value is None or not value.strip():
        return ()
    raw = value.strip()
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
        values = parsed
    elif isinstance(parsed, str):
        values = [parsed]
    else:
        values = re.split(r"\s*[|;,]\s*", raw.strip("{}[]()"))

    return tuple(sorted({str(v).strip().strip("\"'") for v in values if str(v).strip()}))


def artifact(dataset: str) -> Path:
    if dataset not in DATASETS:
        raise ValueError("Unknown dataset. Choose instacart or uci.")
    return MODEL_DIR / f"{dataset}_rules.csv"


def _single(value: str | None) -> tuple[str, ...]:
    if value is None:
        return ()
    value = value.strip()
    return (value,) if value else ()


def _read_rule(row: dict[str, str], schema: str) -> Rule | None:
    if schema == "instacart":
        # Names come directly from Kaggle export; IDs are fallback when names are missing.
        antecedents = _single(
            _field(row, "antecedent_name") or _field(row, "antecedent_id")
        )
        consequents = _single(
            _field(row, "consequent_name") or _field(row, "consequent_id")
        )
    elif schema == "uci":
        # UCI exports StockCode only, not a shared Instacart product namespace.
        antecedents = _single(_field(row, "antecedent_sku"))
        consequents = _single(_field(row, "consequent_sku"))
    else:
        antecedents = _items(
            _field(row, "antecedents", "antecedent", "lhs", "itemsets_a", "if_items")
        )
        consequents = _items(
            _field(row, "consequents", "consequent", "rhs", "itemsets_b", "then_items")
        )

    if not antecedents or not consequents:
        return None
    if {v.casefold() for v in antecedents} & {v.casefold() for v in consequents}:
        return None

    return Rule(
        antecedents=antecedents,
        consequents=consequents,
        support=_number(_field(row, "support", "rule_support")),
        confidence=_number(_field(row, "confidence", "rule_confidence")),
        lift=_number(_field(row, "lift")),
    )


def _schema(headers: list[str]) -> str:
    keys = {_key(h) for h in headers}
    if {"antecedentid", "consequentid"} <= keys:
        return "instacart"
    if {"antecedentsku", "consequentsku"} <= keys:
        return "uci"
    left = {"antecedents", "antecedent", "lhs", "itemsetsa", "ifitems"}
    right = {"consequents", "consequent", "rhs", "itemsetsb", "thenitems"}
    if keys & left and keys & right:
        return "generic"
    raise ValueError(
        f"Unsupported association-rule CSV columns: {headers}. "
        "Expected Instacart *_id/*_name, UCI *_sku, or generic antecedents/consequents."
    )


@lru_cache(maxsize=8)
def _load_cached(path: str, mtime_ns: int, size: int) -> tuple[Rule, ...]:
    del mtime_ns, size  # cache-key only
    rules: list[Rule] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise ValueError(f"Rule CSV has no header: {path}")
        schema = _schema([name.strip() for name in reader.fieldnames])
        for row in reader:
            rule = _read_rule(row, schema)
            if rule is not None:
                rules.append(rule)
    if not rules:
        raise ValueError(f"No valid association rules found in {path}")
    return tuple(rules)


def load_rules(dataset: str) -> tuple[Rule, ...]:
    path = artifact(dataset)
    if not path.is_file():
        raise FileNotFoundError(f"Missing artifact: {path}. Copy notebook output into models/.")
    stat = path.stat()
    return _load_cached(str(path), stat.st_mtime_ns, stat.st_size)


def catalog(dataset: str) -> list[str]:
    products: set[str] = set()
    for rule in load_rules(dataset):
        products.update(rule.antecedents)
        products.update(rule.consequents)
    return sorted(products, key=str.casefold)


def recommend(dataset: str, items: list[str], limit: int) -> dict:
    rules = load_rules(dataset)
    available = {product.casefold(): product for product in catalog(dataset)}
    requested = list(dict.fromkeys(text.strip() for text in items if text.strip()))
    if not requested:
        raise ValueError("Please select at least one product.")
    unknown = [item for item in requested if item.casefold() not in available]
    if unknown:
        raise ValueError(f"Unknown catalog products: {unknown[:5]}. Select from /catalog.")

    selected = {available[item.casefold()] for item in requested}
    selected_folded = {item.casefold() for item in selected}
    matches = 0
    candidates: dict[str, dict] = {}

    for rule in rules:
        if not {item.casefold() for item in rule.antecedents}.issubset(selected_folded):
            continue
        matches += 1
        for product in rule.consequents:
            if product.casefold() in selected_folded:
                continue
            score = next(
                (v for v in (rule.lift, rule.confidence, rule.support) if v is not None),
                None,
            )
            suggestion = {
                "product": product,
                "score": score,
                "support": rule.support,
                "confidence": rule.confidence,
                "lift": rule.lift,
                "matched_input": list(rule.antecedents),
                "source": f"{dataset}_rules.csv",
            }
            existing = candidates.get(product.casefold())
            if existing is None or (score if score is not None else -1) > (
                existing["score"] if existing["score"] is not None else -1
            ):
                candidates[product.casefold()] = suggestion

    suggestions = sorted(
        candidates.values(),
        key=lambda entry: (
            -(entry["score"] if entry["score"] is not None else -1),
            entry["product"].casefold(),
        ),
    )
    return {
        "dataset": dataset,
        "items": sorted(selected),
        "suggestions": suggestions[:limit],
        "matched_rules": matches,
        "scanned_rules": len(rules),
        "disclaimer": (
            "Historical basket association is not causation, purchase probability, "
            "or measured incremental revenue. Human merchandising review required."
        ),
    }


def status() -> dict:
    return {
        dataset: {
            "available": artifact(dataset).is_file(),
            "file": artifact(dataset).name,
        }
        for dataset in DATASETS
    }
