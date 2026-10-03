import os
import sys


def load_local_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")

    if not os.path.exists(env_path):
        print(f"\n❌ Configuration Error: Local .env file missing at {env_path}")
        sys.exit(1)

    config_vars = {}

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                config_vars[key.strip()] = (
                    val.strip().strip('"').strip("'")
                )

    return config_vars


def load_system_prompt():
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "personal_os.md"
    )

    if not os.path.exists(prompt_path):
        print(
            f"\n❌ Configuration Error: "
            f"Personal OS prompt missing at {prompt_path}"
        )
        sys.exit(1)

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read().strip()

    if not prompt:
        print("\n❌ Configuration Error: personal_os.md is empty.")
        sys.exit(1)

    return prompt


ENV = load_local_env()

GEMINI_KEY = ENV.get("GEMINI_API_KEY")
GROQ_KEY = ENV.get("GROQ_API_KEY")

GEMINI_MODEL = "gemini-3.8-flash"

GROQ_MODELS = [
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
]

# Persistent Personal OS instructions.
# This file is intentionally external to the Python code so the
# assistant's operating instructions can evolve without modifying
# the application itself.
SYSTEM_PROMPT = load_system_prompt()
