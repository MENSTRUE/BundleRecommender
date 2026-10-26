"""Optional UCI SKU display metadata, never a model input or prediction.

Uses a verified CSV exported from the original UCI transaction Description field.
Missing mappings remain missing; product identifiers never change.
"""
from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path

from app.core.config import MODEL_DIR

CATALOG_FILENAME = "uci_product_catalog.csv"


@lru_cache(maxsize=8)
def _read_catalog(path: str, mtime_ns: int, size: int) -> dict[str, str]:
    mapping: dict[str, str] = {}
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"stock_code", "description"}.issubset(reader.fieldnames):
            raise ValueError(
                "UCI display catalog requires columns: stock_code, description. "
                "Regenerate with scripts/extract_uci_catalog.py."
            )
        for row in reader:
            sku = (row.get("stock_code") or "").strip().upper()
            description = " ".join((row.get("description") or "").split())
            if sku and description and sku not in mapping:
                mapping[sku] = description
    return mapping


def display_names(dataset: str) -> dict[str, str]:
    if dataset != "uci":
        return {}
    path = MODEL_DIR / CATALOG_FILENAME
    if not path.is_file():
        return {}
    stat = path.stat()
    return _read_catalog(str(path), stat.st_mtime_ns, stat.st_size)


def product_metadata(dataset: str, product_ids: list[str]) -> list[dict[str, str | bool]]:
    names = display_names(dataset)
    return [
        {
            "id": product_id,
            "name": names.get(product_id.upper(), product_id),
            "has_description": product_id.upper() in names,
        }
        for product_id in product_ids
    ]
