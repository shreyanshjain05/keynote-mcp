#!/usr/bin/env python3
"""
Keynote-MCP server launcher (MCP compliant)
"""

import sys
import os
from pathlib import Path
import asyncio

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# -----------------------------
# MCP SAFE LOGGING (STDERR ONLY)
# -----------------------------

def log(msg):
    print(msg, file=sys.stderr, flush=True)


# -----------------------------
# Language via ENV (NO INPUT)
# -----------------------------

LANGUAGE = os.getenv("KEYNOTE_LANG", "en").lower()


def get_messages(lang):
    if lang == "zh":
        return {
            "starting": "Starting Keynote-MCP Server...",
            "env_loaded": "Loaded environment file",
            "env_not_found": ".env not found — using system env",
            "dotenv_missing": "python-dotenv not installed",
            "unsplash_enabled": "Unsplash enabled",
            "unsplash_disabled": "Unsplash disabled",
            "server_failed": "Server startup failed",
            "server_stopped": "Server stopped"
        }
    else:
        return {
            "starting": "Starting Keynote-MCP Server...",
            "env_loaded": "Loaded environment file",
            "env_not_found": ".env not found — using system env",
            "dotenv_missing": "python-dotenv not installed",
            "unsplash_enabled": "Unsplash enabled",
            "unsplash_disabled": "Unsplash disabled",
            "server_failed": "Server startup failed",
            "server_stopped": "Server stopped"
        }


messages = get_messages(LANGUAGE)

# -----------------------------
# Load ENV (silent)
# -----------------------------

try:
    from dotenv import load_dotenv

    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        log(f"{messages['env_loaded']}: {env_path}")
    else:
        log(messages["env_not_found"])

except ImportError:
    log(messages["dotenv_missing"])


# -----------------------------
# Import MCP Server
# -----------------------------

from src.server import main


# -----------------------------
# MCP Entry Point
# -----------------------------

if __name__ == "__main__":
    log(messages["starting"])

    # Unsplash check (stderr only)
    if os.getenv("UNSPLASH_KEY"):
        log(messages["unsplash_enabled"])
    else:
        log(messages["unsplash_disabled"])

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        log(messages["server_stopped"])

    except Exception as e:
        log(f"{messages['server_failed']}: {e}")
        sys.exit(1)
