"""API regression tests with isolated temporary artifacts."""

import csv
from fastapi.testclient import TestClient

from app.main import app
from app.services import rules

client = TestClient(app)


def test_health():
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert 'datasets' in response.json()


def test_catalog_and_recommendation(tmp_path, monkeypatch):
    path = tmp_path / 'instacart_rules.csv'
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=['antecedents', 'consequents', 'support', 'confidence', 'lift'],
        )
        writer.writeheader()
        writer.writerow({
            'antecedents': "frozenset({'milk'})",
            'consequents': "frozenset({'bread'})",
            'support': '0.2',
            'confidence': '0.6',
            'lift': '1.4',
        })

    monkeypatch.setattr(rules, 'MODEL_DIR', tmp_path)
    rules._load_cached.cache_clear()

    catalog_response = client.get('/api/v1/catalog?dataset=instacart')
    assert catalog_response.status_code == 200
    assert catalog_response.json()['products'] == ['bread', 'milk']

    response = client.post('/api/v1/recommend', json={'items': ['milk']})
    assert response.status_code == 200
    assert response.json()['suggestions'][0]['product'] == 'bread'


def test_invalid_dataset():
    assert client.get('/api/v1/catalog?dataset=invalid').status_code == 422


def test_empty_request_rejected():
    assert client.post('/api/v1/recommend', json={'items': []}).status_code == 422
