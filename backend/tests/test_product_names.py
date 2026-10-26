"""Regression tests: product names must never affect recommender identity."""
import csv
from fastapi.testclient import TestClient

from app.main import app
from app.services import rules, product_names

client = TestClient(app)


def write_csv(path, columns, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def test_catalog_details_with_names(tmp_path, monkeypatch):
    write_csv(
        tmp_path / "uci_rules.csv",
        ["antecedent_sku", "consequent_sku", "support", "confidence", "lift"],
        [{"antecedent_sku": "85123A", "consequent_sku": "21733",
          "support": "0.03", "confidence": "0.22", "lift": "5.07"}],
    )
    write_csv(
        tmp_path / "uci_product_catalog.csv",
        ["stock_code", "description"],
        [{"stock_code": "85123A", "description": "Verified holder description"}],
    )
    monkeypatch.setattr(rules, "MODEL_DIR", tmp_path)
    monkeypatch.setattr(product_names, "MODEL_DIR", tmp_path)
    rules._load_cached.cache_clear()
    product_names._read_catalog.cache_clear()

    response = client.get("/api/v1/catalog/details?dataset=uci")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["named_count"] == 1
    by_id = {p["id"]: p for p in data["products"]}
    assert by_id["85123A"]["name"] == "Verified holder description"
    assert by_id["21733"]["name"] == "21733"

    prediction = client.post(
        "/api/v1/recommend", json={"dataset": "uci", "items": ["85123A"]}
    )
    assert prediction.status_code == 200
    assert prediction.json()["suggestions"][0]["product"] == "21733"


def test_missing_catalog_falls_back_to_sku(tmp_path, monkeypatch):
    monkeypatch.setattr(product_names, "MODEL_DIR", tmp_path)
    product_names._read_catalog.cache_clear()
    assert product_names.product_metadata("uci", ["85123A"])[0] == {
        "id": "85123A", "name": "85123A", "has_description": False
    }


def test_other_dataset_keeps_identifiers():
    assert product_names.product_metadata("instacart", ["Banana"])[0]["name"] == "Banana"
