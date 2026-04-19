#!/bin/sh
uv run --with pandas src/load_data.py
uv run fastapi dev src/main.py --host 0.0.0.0
