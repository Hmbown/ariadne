.PHONY: test install dev-install lint format clean help docker-build-prod docker-build-dev docker-push-prod docker-push-dev docker-run-prod compose-dev compose-test

help:
	@echo "Ariadne Development Commands"
	@echo ""
	@echo "  make install      Install package in production mode"
	@echo "  make dev-install  Install package with development dependencies"
	@echo "  make test         Run test suite"
	@echo "  make lint         Check code quality with ruff and mypy"
	@echo "  make format       Format code with ruff and isort"
	@echo "  make clean        Remove build artifacts and cache files"
	@echo "  make docker-build-prod   Build production container image"
	@echo "  make docker-build-dev    Build development container image"
	@echo "  make docker-push-prod    Push production image to GHCR (requires login)"
	@echo "  make docker-push-dev     Push development image to GHCR (requires login)"
	@echo "  make docker-run-prod     Run a quick prod container verification"
	@echo "  make compose-dev         Launch dev compose service"
	@echo "  make compose-test        Run test compose service"

# Container image coordinates (override OWNER on invocation)
OWNER ?= your-gh-username
IMAGE_BASE ?= ghcr.io/$(OWNER)/ariadne-router

install:
	pip install -e .

dev-install:
	pip install -e ".[dev,apple,viz]"

test:
	pytest tests/ -v -n auto

lint:
	@echo "Running ruff..."
	ruff check src/ tests/
	@echo ""
	@echo "Running mypy..."
	mypy src/ariadne/
	@echo ""
	@echo "Lint check complete!"

format:
	@echo "Formatting with ruff..."
	ruff format src/ tests/
	@echo ""
	@echo "Formatting complete!"

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/ htmlcov/ .coverage
	@echo "Clean complete!"

# -----------------------------
# Docker / Compose helpers
# -----------------------------

docker-build-prod:
	docker build --target production -t $(IMAGE_BASE):latest .

docker-build-dev:
	docker build --target development -t $(IMAGE_BASE):dev .

docker-push-prod:
	docker push $(IMAGE_BASE):latest

docker-push-dev:
	docker push $(IMAGE_BASE):dev

docker-run-prod:
	docker run --rm $(IMAGE_BASE):latest python -c "import ariadne; print('Ariadne OK:', ariadne.__version__)"

compose-dev:
	docker-compose up -d ariadne-dev

compose-test:
	docker-compose up --abort-on-container-exit ariadne-test
