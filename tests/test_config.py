from pathlib import Path

from app import config


def test_load_config_examples(tmp_path):
    csv_path = Path("data/examples/in_scope.csv")
    burp_path = Path("data/examples/burp_project.json")
    schema_path = Path("schemas/burp_project.schema.json")
    targets = config.load_csv(csv_path)
    burp = config.load_burp(burp_path, schema_path)
    assert targets[0].host == "example.com"
    assert burp.headers["X-Test"] == "1"
