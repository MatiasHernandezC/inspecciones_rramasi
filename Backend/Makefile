# Variables
TIMEOUT ?= 60
MODEL_PATH ?= ./ml/model/
MODEL_NAME ?= model.pkl

APP_NAME := app.main:app
UV := uv run
ALEMBIC := $(UV) alembic
PYTHONPATH := app/

.PHONY: all clean test install run deploy down alembic-init alembic-rev alembic-up alembic-downgrade

# Workflow por defecto
all: install run

venv:
	uv venv .venv

install: venv
	pip install uv --break-system-packages || pip install uv
	uv pip install -e ".[dev]"
	if not exist .env copy .env.example .env

run:
	uvicorn app.main:app --reload
deploy:
	docker-compose build
	docker-compose up -d

down:
	docker-compose down

# ---- Alembic ----
alembic-init:
	$(ALEMBIC) init alembic

alembic-rev:
	$(ALEMBIC) revision --autogenerate -m "$(m)"

alembic-up:
	$(ALEMBIC) upgrade head

alembic-downgrade:
	$(ALEMBIC) downgrade -1

test: install
	$(UV) pytest tests -vv --show-capture=all

clean:
	-del /s /q *.pyc
	-del /s /q __pycache__
	-del /s /q .cache build dist *.egg-info htmlcov .tox docs\_build
