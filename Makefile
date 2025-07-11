install:
	pip install -r requirements.txt

test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

coverage:
	pytest --cov=src/task_manager --cov-report=html --cov-report=term-missing

clean:
	rm -rf .pytest_cache htmlcov *.pyc __pycache__

lint:
	flake8 src/ tests/

all: install lint test coverage
