"""
Constantes generales de THE ODIN PROJECT.
"""

# ==========================================
# SYSTEM
# ==========================================

PROJECT_NAME = "THE ODIN PROJECT"
DEFAULT_VERSION = "0.1.0"

# ==========================================
# ENVIRONMENTS
# ==========================================

ENV_DEVELOPMENT = "development"
ENV_TESTING = "testing"
ENV_PRODUCTION = "production"

# ==========================================
# AI PROVIDERS
# ==========================================

PROVIDER_GEMINI = "gemini"
PROVIDER_GROQ = "groq"

# ==========================================
# BOT ROLES
# ==========================================

ROLE_SUPERVISOR = "supervisor"

WORKER_1 = "worker_1"
WORKER_2 = "worker_2"
WORKER_3 = "worker_3"
WORKER_4 = "worker_4"
WORKER_5 = "worker_5"

# ==========================================
# GENERAL TASK STATES
# ==========================================

TASK_PENDING = "PENDING"
TASK_ANALYZING = "ANALYZING"
TASK_WORKING = "WORKING"
TASK_TESTING = "TESTING"
TASK_WAITING_APPROVAL = "WAITING_APPROVAL"
TASK_COMPLETED = "COMPLETED"
TASK_FAILED = "FAILED"
TASK_PAUSED = "PAUSED"
TASK_STOPPED = "STOPPED"

# ==========================================
# SECURITY
# ==========================================

ACTION_ALLOWED = "ALLOWED"
ACTION_REQUIRES_APPROVAL = "REQUIRES_APPROVAL"
ACTION_DENIED = "DENIED"

# ==========================================
# RESOURCE STATES
# ==========================================

RESOURCE_AVAILABLE = "AVAILABLE"
RESOURCE_LIMIT = "RESOURCE_LIMIT"
RESOURCE_ERROR = "RESOURCE_ERROR"

# ==========================================
# EMERGENCY CONTROL
# ==========================================

COMMAND_STOP_ALL = "STOP ALL"
COMMAND_PAUSE = "PAUSE"
COMMAND_RESUME = "RESUME"
