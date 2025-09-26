#!/usr/bin/env bash
set -euo pipefail

# --- Einstellungen ---
MIN_PIP_VERSION="24.0"   # Mindestversion für pip

# --- Pfade ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"
REQ_FILE="requirements.txt"
REQ_HASH_FILE="$VENV_DIR/.requirements.sha256"

DID_CHANGE=0

# --- venv erstellen falls nötig ---
if [ ! -d "$VENV_DIR" ]; then
  echo "[setup] creating virtual environment..."
  python3 -m venv "$VENV_DIR"
  NEW_VENV=1
  DID_CHANGE=1
else
  NEW_VENV=0
fi

# Aktivieren
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# pip eigene versionchecks ausschalten
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_NO_INPUT=1

# --- Helfer: pip-upgrade nötig? ---
need_pip_upgrade() {
  python - "$MIN_PIP_VERSION" "$REQ_FILE" <<'PY'
import sys, re
from pathlib import Path
min_version = sys.argv[1]
req_file = Path(sys.argv[2])
try:
    import pip
    from packaging.version import Version
    from packaging.specifiers import SpecifierSet
except Exception:
    sys.exit(0)  # packaging fehlt → upgrade

cur = Version(pip.__version__)
if cur < Version(min_version):
    sys.exit(0)

if req_file.is_file():
    pat = re.compile(r'^\s*pip\s*([<>=!~]=[^#\s]+.*)?$', re.IGNORECASE)
    for line in req_file.read_text().splitlines():
        m = pat.match(line)
        if not m: continue
        spec_str = (m.group(1) or "").strip()
        if spec_str:
            try:
                if Version(pip.__version__) not in SpecifierSet(spec_str):
                    sys.exit(0)
            except Exception:
                pass
sys.exit(1)
PY
}

# --- pip ggf. aktualisieren ---
if need_pip_upgrade; then
  echo "[setup] upgrading pip..."
  python -m pip install --upgrade pip
  DID_CHANGE=1
fi

# --- requirements ggf. installieren ---
install_deps_if_needed() {
  [ -f "$REQ_FILE" ] || return 0

  if command -v sha256sum >/dev/null 2>&1; then
    CURRENT_HASH="$(sha256sum "$REQ_FILE" | awk '{print $1}')"
  else
    CURRENT_HASH="$(shasum -a 256 "$REQ_FILE" | awk '{print $1}')"
  fi

  NEED_INSTALL=0
  if [ "$NEW_VENV" -eq 1 ] || [ ! -f "$REQ_HASH_FILE" ]; then
    NEED_INSTALL=1
  else
    SAVED_HASH="$(cat "$REQ_HASH_FILE" 2>/dev/null || true)"
    if [ "$CURRENT_HASH" != "$SAVED_HASH" ]; then
      NEED_INSTALL=1
    else
      if ! pip check >/dev/null 2>&1; then
        NEED_INSTALL=1
      fi
    fi
  fi

  if [ "$NEED_INSTALL" -eq 1 ]; then
    echo "[setup] installing dependencies..."
    pip install -r "$REQ_FILE"
    printf '%s\n' "$CURRENT_HASH" > "$REQ_HASH_FILE"
    DID_CHANGE=1
  fi
}

install_deps_if_needed

# --- Start ---
exec python timey.py "$@"