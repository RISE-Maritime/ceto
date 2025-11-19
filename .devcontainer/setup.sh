#!/bin/bash
set -e

echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

echo "Creating virtual environment and installing dependencies..."
uv venv
source .venv/bin/activate

echo "Installing project in editable mode with all dependencies..."
uv pip install -e ".[dev]"

echo "Setup complete! Virtual environment is ready at .venv"
echo "To activate: source .venv/bin/activate"
