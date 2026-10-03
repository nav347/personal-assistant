import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================================
# Environment
# ============================================================================

def load_local_env():
    env_path = os.path.join(
        BASE_DIR,
        ".env"
    )

    if not os.path.exists(env_path):
        print(
            f"\n❌ Configuration Error: "
            f"Local .env file missing at {env_path}"
        )
        sys.exit(1)

    values = {}

    with open(
        env_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:
            line = line.strip()

            if (
                line
                and not line.startswith("#")
                and "=" in line
            ):
                key, value = line.split("=", 1)

                values[key.strip()] = (
                    value.strip()
                    .strip('"')
                    .strip("'")
                )

    return values


ENV = load_local_env()

GEMINI_KEY = ENV.get("GEMINI_API_KEY")
GROQ_KEY = ENV.get("GROQ_API_KEY")


# ============================================================================
# Provider configuration
# ============================================================================

PROVIDER_ORDER = [
    "gemini",
    "groq",
]


# Keep this list limited to models we have intentionally configured.
#
# More providers/models can be added later without changing the harness.

GEMINI_MODELS = [
    "gemini-3.8-flash",
]


GROQ_MODELS = [
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
]


# ============================================================================
# Network / failover behavior
# ============================================================================

REQUEST_TIMEOUT = 30

# A model that receives 429 should not immediately be hammered again.
RATE_LIMIT_COOLDOWN = 60

# Temporary server-side problems.
SERVER_ERROR_COOLDOWN = 20

# Network failures.
NETWORK_COOLDOWN = 15

# Timeouts.
TIMEOUT_COOLDOWN = 30

# Invalid model / bad configuration / authorization problems.
CONFIG_ERROR_COOLDOWN = 300


# ============================================================================
# Personal OS
# ============================================================================

def load_system_prompt():
    prompt_path = os.path.join(
        BASE_DIR,
        "personal_os.md"
    )

    if not os.path.exists(prompt_path):
        print(
            f"\n❌ Configuration Error: "
            f"Personal OS prompt missing at {prompt_path}"
        )
        sys.exit(1)

    with open(
        prompt_path,
        "r",
        encoding="utf-8"
    ) as file:

        prompt = file.read().strip()

    if not prompt:
        print(
            "\n❌ Configuration Error: "
            "personal_os.md is empty."
        )
        sys.exit(1)

    return prompt


SYSTEM_PROMPT = load_system_prompt()
