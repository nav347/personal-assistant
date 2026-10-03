import requests
import config


# ---------------------------------------------------------------------------
# Provider helpers
# ---------------------------------------------------------------------------

def call_gemini(messages):
    """
    Call Gemini.

    Important:
    Gemini rate limits (429) must NOT block the interactive CLI with
    long foreground sleeps. A transient provider failure simply causes
    the cascade to try the next provider.
    """

    if not config.GEMINI_KEY:
        return None, "Gemini Key Missing"

    model = getattr(
        config,
        "GEMINI_MODEL",
        "gemini-3.8-flash"
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

    for m in messages:
        role = m.get("role")

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
                    "text": m.get("content", "")
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
        res = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        # Rate limit:
        # Do NOT sleep/retry here. Return immediately so the cascade
        # can continue to Groq.
        if res.status_code == 429:
            print(
                f"\n[DEBUG] Gemini HTTP 429 "
                f"(rate limited; falling back immediately)"
            )
            return None, "Gemini HTTP 429"

        if res.status_code in (500, 502, 503, 504):
            print(
                f"\n[DEBUG] Gemini HTTP {res.status_code} "
                f"(temporary provider failure; falling back)"
            )
            return None, f"Gemini HTTP {res.status_code}"

        if res.status_code == 200:
            data = res.json()

            candidates = data.get("candidates", [])

            if candidates:
                parts = (
                    candidates[0]
                    .get("content", {})
                    .get("parts", [])
                )

                text_parts = [
                    part.get("text", "")
                    for part in parts
                    if part.get("text")
                ]

                if text_parts:
                    return (
                        "\n".join(text_parts),
                        f"Gemini ({model})"
                    )

            return None, "Gemini returned no text"

        try:
            error_data = res.json()
            error_message = (
                error_data
                .get("error", {})
                .get("message", str(error_data))
            )
        except Exception:
            error_message = res.text[:300]

        return (
            None,
            f"Gemini HTTP {res.status_code}: "
            f"{error_message[:300]}"
        )

    except requests.Timeout:
        return None, "Gemini Timeout"

    except requests.RequestException as e:
        return None, f"Gemini Network Error ({str(e)[:200]})"

    except Exception as e:
        return None, f"Gemini Crash ({str(e)[:200]})"


# ---------------------------------------------------------------------------
# Groq
# ---------------------------------------------------------------------------

def call_groq(messages):
    """
    Call Groq using the existing JSON-command architecture.

    We deliberately do NOT send native function/tool definitions here.
    The Python harness currently owns tool execution through tools.py.

    This prevents the model from inventing <tool_call> blocks that
    assistant.py cannot execute.
    """

    if not config.GROQ_KEY:
        return None, "Groq Key Missing"

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

    for m in messages:
        role = m.get("role")

        if role not in ("user", "assistant"):
            continue

        formatted_messages.append({
            "role": role,
            "content": m.get("content", "")
        })

    models_to_try = getattr(
        config,
        "GROQ_MODELS",
        ["openai/gpt-oss-20b"]
    )

    for model in models_to_try:

        payload = {
            "model": model,
            "messages": formatted_messages,
            "temperature": 0.2
        }

        try:
            res = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if res.status_code == 429:
                print(
                    f"\n[DEBUG] Groq model={model} "
                    f"HTTP=429 "
                    f"(rate limited; trying next model)"
                )
                continue

            if res.status_code in (500, 502, 503, 504):
                print(
                    f"\n[DEBUG] Groq model={model} "
                    f"HTTP={res.status_code} "
                    f"(temporary failure; trying next model)"
                )
                continue

            if res.status_code == 200:
                data = res.json()

                choices = data.get("choices", [])

                if choices:
                    message = choices[0].get("message", {})
                    content = message.get("content")

                    if content:
                        return (
                            content,
                            f"Groq ({model})"
                        )

                    # Some OpenAI-compatible responses can expose
                    # tool calls separately. Since this harness does
                    # not currently execute native Groq tools, don't
                    # pretend that such a call happened.
                    tool_calls = message.get("tool_calls")

                    if tool_calls:
                        print(
                            f"\n[DEBUG] Groq model={model} "
                            f"returned native tool_calls, but the "
                            f"current harness does not expose native "
                            f"tools to this request."
                        )

                        continue

                print(
                    f"\n[DEBUG] Groq returned no usable content "
                    f"for {model}"
                )
                continue

            try:
                error_data = res.json()
                error_message = (
                    error_data
                    .get("error", {})
                    .get("message", str(error_data))
                )
            except Exception:
                error_message = res.text[:300]

            print(
                f"\n[DEBUG] Groq model={model} "
                f"HTTP={res.status_code} "
                f"ERROR={str(error_message)[:300]}"
            )

        except requests.Timeout:
            print(
                f"\n[DEBUG] Groq timeout for model {model}"
            )

        except requests.RequestException as e:
            print(
                f"\n[DEBUG] Groq network error for {model}: "
                f"{str(e)[:200]}"
            )

        except Exception as e:
            print(
                f"\n[DEBUG] Groq exception for {model}: "
                f"{str(e)[:200]}"
            )

    return None, "Groq FAILED"
