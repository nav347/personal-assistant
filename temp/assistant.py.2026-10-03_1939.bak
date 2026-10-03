import sys
import json
import config
import api_clients
import diagnostics
import tools


def get_user_input():
    """
    Normal mode:
        Type one line and press Enter.

    Multiline mode:
        Type /paste
        Paste/type anything, including blank lines.
        Finish with /end.
    """

    try:
        first_line = input("✨ User ➔ ")

        if first_line.strip().lower() in ("exit", "quit"):
            return None

        if first_line.strip().lower() == "/paste":
            print("📋 Paste mode enabled.")
            print("Finish with /end on its own line.")
            print("Blank lines are allowed.")
            print("Type /cancel to discard.\n")

            lines = []

            while True:
                try:
                    line = input()

                except KeyboardInterrupt:
                    print("\n❌ Paste cancelled.\n")
                    return ""

                except EOFError:
                    print("\n📨 End of input.")
                    break

                if line.strip() == "/end":
                    break

                if line.strip() == "/cancel":
                    print("❌ Paste cancelled.\n")
                    return ""

                lines.append(line)

            message = "\n".join(lines)

            print(
                f"📨 Multiline message received: "
                f"{len(lines)} lines / {len(message)} characters\n"
            )

            return message

        return first_line

    except KeyboardInterrupt:
        print("\n")
        return ""

    except EOFError:
        print("\n👋 Session ended.")
        return None


def cascade_llm(messages, gemini_ok, groq_ok):
    if gemini_ok:
        reply, active_model = api_clients.call_gemini(messages)
        if reply:
            return reply, active_model

    if groq_ok:
        reply, active_model = api_clients.call_groq(messages)
        if reply:
            return reply, active_model

    print(
        "\n❌ LLM request failed. "
        "Returning to the user prompt instead of exiting."
    )

    return None, None


def main():
    gemini_ok, groq_ok = diagnostics.run_startup_checks()

    if not gemini_ok and not groq_ok:
        print("❌ No working LLM providers available.")
        sys.exit(1)

    print("🤖 INTERACTIVE CONVERSATIONAL AGENT ONLINE")
    print("Type 'exit' or 'quit' to close.")
    print("Type '/paste' for multiline input.\n")

    messages = []

    while True:
        user_input = get_user_input()

        if user_input is None:
            break

        if not user_input.strip():
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        response_text, active_model = cascade_llm(
            messages,
            gemini_ok,
            groq_ok
        )

        # IMPORTANT:
        # Never exit the application just because an LLM request failed.
        if response_text is None:
            messages.pop()
            continue

        messages.append({
            "role": "assistant",
            "content": response_text
        })

        try:
            exec_data = json.loads(response_text.strip())

            if "command" in exec_data:
                print(
                    f"\n🧠 Agent Layer [{active_model}]: "
                    f"{exec_data.get('thought', '')}"
                )

                print(
                    f"💻 Shell Action: "
                    f"{exec_data['command']}"
                )

                output = tools.execute_bash(
                    exec_data["command"]
                )

                terminal_output = (
                    output["stdout"]
                    if output["stdout"]
                    else output["stderr"]
                )

                print(
                    f"📊 Terminal Output:\n"
                    f"{terminal_output}\n"
                )

                messages.append({
                    "role": "user",
                    "content": (
                        f"Terminal Result "
                        f"(Exit Code {output['code']}):\n"
                        f"STDOUT:\n{output['stdout']}\n"
                        f"STDERR:\n{output['stderr']}"
                    )
                })

                final_reply, final_model = cascade_llm(
                    messages,
                    gemini_ok,
                    groq_ok
                )

                if final_reply is not None:
                    print(
                        f"🤖 Assistant ➔ {final_reply}\n"
                    )

                    messages.append({
                        "role": "assistant",
                        "content": final_reply
                    })

            else:
                print(
                    f"\n🤖 {active_model} ➔ "
                    f"{response_text}\n"
                )

        except json.JSONDecodeError:
            print(
                f"\n🤖 {active_model} ➔ "
                f"{response_text}\n"
            )


if __name__ == "__main__":
    main()
