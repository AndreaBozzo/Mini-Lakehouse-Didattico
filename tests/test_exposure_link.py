from pathlib import Path

import pytest
import requests
import yaml

EXPOSURES_PATH = Path("dbt/models/exposures/exposures.yml")  # adatta al tuo path


def get_exposure_urls(yaml_path):
    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    exposures = []
    if isinstance(data, dict):
        exposures = data.get("exposures", [])
    elif isinstance(data, list):
        exposures = data
    return [
        exp["url"]
        for exp in exposures
        if isinstance(exp, dict)
        and "url" in exp
        and isinstance(exp["url"], str)
        and exp["url"].startswith("http")
    ]


@pytest.mark.parametrize("url", get_exposure_urls(EXPOSURES_PATH))
def test_exposure_url_accessible(url):
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code < 400
    except Exception as e:
        pytest.fail(f"Impossibile raggiungere URL exposure: {url} → {e}")
