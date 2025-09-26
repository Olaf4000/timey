#!/bin/bash
# exit on error
set -e

# Absoluten Pfad zum Ordner dieses Scripts bestimmen
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# In Projektordner wechseln (damit requirements.txt & venv stimmen)
cd "$SCRIPT_DIR"

# Virtuelle Umgebung erstellen falls nicht vorhanden
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Aktivieren
source .venv/bin/activate

# pip updaten
pip install --upgrade pip

# Abhängigkeiten installieren falls requirements.txt existiert
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Python-Skript starten + Parameter durchreichen
echo "Starting application..."
python timey.py "$@"