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

echo "Activating virtual environment on terminal start..."
echo 'source /workspaces/ceto/.venv/bin/activate' >> /home/vscode/.bashrc