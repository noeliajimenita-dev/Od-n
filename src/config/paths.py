"""
Rutas principales de THE ODIN PROJECT.

Las rutas se calculan a partir de la ubicación del proyecto
para evitar depender de rutas específicas del dispositivo.
"""

from pathlib import Path


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ==========================================
# MAIN DIRECTORIES
# ==========================================

SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"


# ==========================================
# RUNTIME DIRECTORIES
# ==========================================

DATA_DIR = PROJECT_ROOT / "data"
RUNTIME_DIR = DATA_DIR / "runtime"
LOCAL_DATA_DIR = DATA_DIR / "local"

LOGS_DIR = PROJECT_ROOT / "logs"
TEMP_DIR = PROJECT_ROOT / "tmp"


# ==========================================
# SECURITY
# ==========================================

SECRETS_DIR = PROJECT_ROOT / "secrets"


# ==========================================
# GENERATED FILES
# ==========================================

GENERATED_DIR = PROJECT_ROOT / "generated"


def get_project_root() -> Path:
    """Devuelve la raíz del proyecto."""
    return PROJECT_ROOT
