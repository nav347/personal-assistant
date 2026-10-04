import time
import requests
import config


# ============================================================================
# Provider State
# ============================================================================

# model_key -> unix timestamp until which the model should be skipped
_COOLDOWNS = {}


def _now():
    return time.time()


def _cooldown(model_key, seconds):
    _COOLDOWNS[model_key] = _now() + seconds


def _is_cooled_down(model_key):
    until = _COOLDOWNS.get(model_key, 0)

    if until <= _now():
        _COOLDOWNS.pop(model_key, None)
        return False

    return True


def _remaining_cooldown(model_key):
    until = _COOLDOWNS.get(model_key, 0)
    return max(0, int(until - _now()))


# ============================================================================
# Response helpers
# ============================================================================

def _error_message(response):
    try:
        data = response.json()

        error = data.get("error", {})

        if isinstance(error, dict):
            return str(
                error.get(
                    "message",
                    error
                )
            )

        return str(error)

    except Exception:
        return response.text[:300]


def _extract_gemini_text(data):
    candidates = data.get("candidates", [])

    for candidate in candidates:
        content = candidate.get("content", {})
        parts = content.get("parts", [])

        text_parts = []

        for part in parts:
            text_value = part.get("text")

            if text_value:
                text_parts.append(text_value)

        if text_parts:
            return "\n".join(text_parts)

    return None


def _extract_openai_text(data):
    choices = data.get("choices", [])

    if not choices:
        return None

    message = choices[0].get("message", {})

    content = message.get("content")

    if isinstance(content, str) and content.strip():
        return content

    return None


# ============================================================================
# Gemini
# ============================================================================

def _call_gemini_model(messages, model):
    if not config.GEMINI_KEY:
        return None, "Gemini key missing"

    model_key = f"gemini:{model}"

    if _is_cooled_down(model_key):
        return None, (
            f"Gemini {model} cooling down "
            f"({_remaining_cooldown(model_key)}s)"
        )

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent"
    )

    headers = {
        "x-goog-api-key": config.GEMINI_KEY,
        "Content-Type": "application/json",
    }

    contents = []

    for message in messages:
        role = message.get("role")

        if role == "system":
            continue

        if role == "assistant":
            role = "model"

        if role not in ("user", "model"):
            continue

        contents.append({
            "role": role,
            "parts": [
                {
                    "text": message.get("content", "")
                }
            ]
        })

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [
                {
                    "text": config.SYSTEM_PROMPT
                }
            ]
        },
        "generationConfig": {
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=config.REQUEST_TIMEOUT
        )

    except requests.Timeout:
        _cooldown(model_key, config.TIMEOUT_COOLDOWN)

        return None, f"Gemini {model} timeout"

    except requests.RequestException as exc:
        _cooldown(model_key, config.NETWORK_COOLDOWN)

        return None, (
            f"Gemini {model} network error: "
            f"{str(exc)[:200]}"
        )

    except Exception as exc:
        return None, (
            f"Gemini {model} exception: "
            f"{str(exc)[:200]}"
        )

    status = response.status_code

    if status == 200:
        try:
            data = response.json()
        except Exception as exc:
            return None, (
                f"Gemini {model} invalid JSON: "
                f"{str(exc)[:200]}"
            )

        text = _extract_gemini_text(data)

        if text:
            return text, f"Gemini ({model})"

        return None, f"Gemini {model} returned no text"

    if status == 429:
        _cooldown(model_key, config.RATE_LIMIT_COOLDOWN)

        return None, f"Gemini {model} rate limited"

    if status in (400, 401, 403, 404):
        # These are generally configuration/model/key problems.
        # Cool down longer so we don't repeatedly hammer a bad entry.
        _cooldown(model_key, config.CONFIG_ERROR_COOLDOWN)

        return None, (
            f"Gemini {model} HTTP {status}: "
            f"{_error_message(response)[:250]}"
        )

    if status in (500, 502, 503, 504):
        _cooldown(model_key, config.SERVER_ERROR_COOLDOWN)

        return None, (
            f"Gemini {model} temporary HTTP {status}"
        )

    return None, (
        f"Gemini {model} HTTP {status}: "
        f"{_error_message(response)[:250]}"
    )


def call_gemini(messages):
    models = getattr(
        config,
        "GEMINI_MODELS",
        []
    )

    for model in models:
        reply, status = _call_gemini_model(
            messages,
            model
        )

        if reply:
            return reply, status

    return None, "Gemini cluster unavailable"


# ============================================================================
# Groq
# ============================================================================

def _call_groq_model(messages, model):
    if not config.GROQ_KEY:
        return None, "Groq key missing"

    model_key = f"groq:{model}"

    if _is_cooled_down(model_key):
        return None, (
            f"Groq {model} cooling down "
            f"({_remaining_cooldown(model_key)}s)"
        )

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {config.GROQ_KEY}",
        "Content-Type": "application/json",
    }

    formatted_messages = [
        {
            "role": "system",
            "content": config.SYSTEM_PROMPT
        }
    ]

    for message in messages:
        role = message.get("role")

        if role not in ("user", "assistant"):
            continue

        formatted_messages.append({
            "role": role,
            "content": message.get("content", "")
        })

    payload = {
        "model": model,
        "messages": formatted_messages,
        "temperature": 0.2
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=config.REQUEST_TIMEOUT
        )

    except requests.Timeout:
        _cooldown(model_key, config.TIMEOUT_COOLDOWN)

        return None, f"Groq {model} timeout"

    except requests.RequestException as exc:
        _cooldown(model_key, config.NETWORK_COOLDOWN)

        return None, (
            f"Groq {model} network error: "
            f"{str(exc)[:200]}"
        )

    except Exception as exc:
        return None, (
            f"Groq {model} exception: "
            f"{str(exc)[:200]}"
        )

    status = response.status_code

    if status == 200:
        try:
            data = response.json()
        except Exception as exc:
            return None, (
                f"Groq {model} invalid JSON: "
                f"{str(exc)[:200]}"
            )

        text = _extract_openai_text(data)

        if text:
            return text, f"Groq ({model})"

        return None, f"Groq {model} returned no text"

    if status == 429:
        _cooldown(model_key, config.RATE_LIMIT_COOLDOWN)

        return None, f"Groq {model} rate limited"

    if status in (400, 401, 403, 404):
        _cooldown(model_key, config.CONFIG_ERROR_COOLDOWN)

        return None, (
            f"Groq {model} HTTP {status}: "
            f"{_error_message(response)[:250]}"
        )

    if status in (500, 502, 503, 504):
        _cooldown(model_key, config.SERVER_ERROR_COOLDOWN)

        return None, (
            f"Groq {model} temporary HTTP {status}"
        )

    return None, (
        f"Groq {model} HTTP {status}: "
        f"{_error_message(response)[:250]}"
    )


def call_groq(messages):
    models = getattr(
        config,
        "GROQ_MODELS",
        []
    )

    for model in models:
        reply, status = _call_groq_model(
            messages,
            model
        )

        if reply:
            return reply, status

    return None, "Groq cluster unavailable"


# ============================================================================
# Unified Provider Cascade
# ============================================================================

def call_llm(messages):
    """
    Unified model gateway.

    Providers are attempted in configured order.

    A failed model never blocks the interactive session.
    A successful model immediately ends the cascade.
    """

    providers = getattr(
        config,
        "PROVIDER_ORDER",
        ["gemini", "groq"]
    )

    failures = []

    for provider in providers:

        if provider == "gemini":
            reply, status = call_gemini(messages)

        elif provider == "groq":
            reply, status = call_groq(messages)

        else:
            failures.append(
                f"Unknown provider: {provider}"
            )
            continue

        if reply:
            return reply, status

        failures.append(status)

    return None, " | ".join(failures)


# ============================================================================
# Diagnostics
# ============================================================================

def provider_status():
    """
    Return local provider/model state without making an API request.
    """

    result = []

    for provider in getattr(
        config,
        "PROVIDER_ORDER",
        []
    ):

        if provider == "gemini":
            models = getattr(
                config,
                "GEMINI_MODELS",
                []
            )

        elif provider == "groq":
            models = getattr(
                config,
                "GROQ_MODELS",
                []
            )

        else:
            models = []

        for model in models:
            key = f"{provider}:{model}"

            if _is_cooled_down(key):
                state = (
                    f"cooldown "
                    f"{_remaining_cooldown(key)}s"
                )
            else:
                state = "ready"

            result.append({
                "provider": provider,
                "model": model,
                "state": state
            })

    return result
