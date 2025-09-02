install:
pip install .

run:
bbscan run --in-scope data/examples/in_scope.csv --burp data/examples/burp_project.json --out out/ --dry-run

test:
pytest

lint:
ruff app tests
