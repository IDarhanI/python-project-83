PORT ?= 8000

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

lint:
	uv run ruff check .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

fix:  # ДОБАВЛЯЕМ ЭТУ КОМАНДУ
	uv run ruff check --fix . && uv run ruff format .

test:
	uv run pytest tests/ -v

.PHONY: install dev start render-start build lint format format-check fix test