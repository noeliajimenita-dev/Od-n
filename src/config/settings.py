import os


def get_env(name: str, default: str = "") -> str:
    """Obtiene una variable de entorno sin exponer secretos."""
    return os.getenv(name, default)


# ==========================================
# APPLICATION
# ==========================================

APP_NAME = get_env("APP_NAME", "THE_ODIN_PROJECT")
APP_ENV = get_env("APP_ENV", "development")
APP_VERSION = get_env("APP_VERSION", "0.1.0")
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")


# ==========================================
# AI PROVIDERS
# ==========================================

GEMINI_API_KEY = get_env("GEMINI_API_KEY")
GROQ_API_KEY = get_env("GROQ_API_KEY")


# ==========================================
# TELEGRAM
# ==========================================

TELEGRAM_SUPERVISOR_BOT_TOKEN = get_env(
    "TELEGRAM_SUPERVISOR_BOT_TOKEN"
)

TELEGRAM_WORKER_1_BOT_TOKEN = get_env(
    "TELEGRAM_WORKER_1_BOT_TOKEN"
)

TELEGRAM_WORKER_2_BOT_TOKEN = get_env(
    "TELEGRAM_WORKER_2_BOT_TOKEN"
)

TELEGRAM_WORKER_3_BOT_TOKEN = get_env(
    "TELEGRAM_WORKER_3_BOT_TOKEN"
)

TELEGRAM_WORKER_4_BOT_TOKEN = get_env(
    "TELEGRAM_WORKER_4_BOT_TOKEN"
)

TELEGRAM_WORKER_5_BOT_TOKEN = get_env(
    "TELEGRAM_WORKER_5_BOT_TOKEN"
)


# ==========================================
# GITHUB
# ==========================================

GITHUB_TOKEN = get_env("GITHUB_TOKEN")
GITHUB_REPOSITORY = get_env("GITHUB_REPOSITORY")
GITHUB_MAIN_BRANCH = get_env(
    "GITHUB_MAIN_BRANCH",
    "main"
)


# ==========================================
# RESOURCE LIMITS
# ==========================================

DAILY_TOKEN_LIMIT = int(
    get_env("DAILY_TOKEN_LIMIT", "0")
)

MONTHLY_TOKEN_LIMIT = int(
    get_env("MONTHLY_TOKEN_LIMIT", "0")
)

SAFETY_RESERVE_PERCENT = int(
    get_env("SAFETY_RESERVE_PERCENT", "10")
)


# ==========================================
# SYSTEM CONTROL
# ==========================================

STOP_ALL_ENABLED = (
    get_env("STOP_ALL_ENABLED", "true").lower()
    == "true"
)

HUMAN_APPROVAL_REQUIRED = (
    get_env("HUMAN_APPROVAL_REQUIRED", "true").lower()
    == "true"
)

PROTECTED_MAIN = (
    get_env("PROTECTED_MAIN", "true").lower()
    == "true"
)

AUDIT_LOG_ENABLED = (
    get_env("AUDIT_LOG_ENABLED", "true").lower()
    == "true"
)

BACKUP_BEFORE_CHANGES = (
    get_env("BACKUP_BEFORE_CHANGES", "true").lower()
    == "true"
)


# ==========================================
# ORACLE CLOUD
# ==========================================

ORACLE_HOST = get_env("ORACLE_HOST")
ORACLE_USERNAME = get_env("ORACLE_USERNAME")
ORACLE_SSH_KEY_PATH = get_env("ORACLE_SSH_KEY_PATH")
