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

LANGUAGE = os.getenv("KEYNOTE_LANG")


def get_messages(lang):
    if lang == "zh":
        return {
            "starting": "🚀 启动 Keynote-MCP 服务器...",
            "env_loaded": "📄 已加载环境变量文件",
            "env_not_found": "📄 未找到 .env 文件，使用系统环境变量",
            "dotenv_missing": "⚠️  python-dotenv 未安装，仅使用系统环境变量",
            "unsplash_enabled": "🖼️  Unsplash 配图功能已启用",
            "unsplash_disabled": "⚠️  未检测到 UNSPLASH_KEY 环境变量",
            "server_failed": "❌ 服务器启动失败",
            "server_stopped": "👋 服务器已停止"
        }
    else:  # English
        return {
            "starting": "🚀 Starting Keynote-MCP Server...",
            "env_loaded": "📄 Environment variables loaded from file",
            "env_not_found": "📄 .env file not found, using system environment variables",
            "dotenv_missing": "⚠️  python-dotenv not installed, using system environment variables only",
            "unsplash_enabled": "🖼️  Unsplash image feature is enabled",
            "unsplash_disabled": "⚠️  UNSPLASH_KEY environment variable not detected",
            "server_failed": "❌ Server startup failed",
            "server_stopped": "👋 Server stopped"
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
