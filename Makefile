.PHONY: install test lint docker clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --tb=short

test-coverage:
	pytest tests/ --cov=phantom_veil --cov-report=html

lint:
	flake8 phantom_veil/ --max-line-length=120
	mypy phantom_veil/ --ignore-missing-imports

docker:
	docker build -t phantom-veil .

docker-run:
	docker compose up -d

docker-stop:
	docker compose down

clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	find . -name "*.pyc" -delete
