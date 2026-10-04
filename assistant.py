import sys
import json
import api_clients
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


def print_provider_status():
    print("\n📡 Provider Gateway")

    for item in api_clients.provider_status():
        print(
            f"  {item['provider']:8} "
            f"{item['model']:35} "
            f"{item['state']}"
        )

    print()


def run_agent_turn(messages):
    """
    Send one conversational turn through the single unified gateway.

    Provider selection, cooldowns, failover, and model routing all
    belong inside api_clients.py.
    """

    return api_clients.call_llm(messages)


def main():
    print("=============================================================")
    print("🤖 PERSONAL OS AGENT")
    print("=============================================================")
    print("Type 'exit' or 'quit' to close.")
    print("Type '/paste' for multiline input.")
    print("Type '/status' to inspect provider state.")
    print()

    # Do NOT make API requests at startup.
    #
    # Startup health checks can consume quota and can themselves
    # trigger rate limits. The gateway will discover availability
    # when an actual request is made.
    print_provider_status()

    messages = []

    while True:
        user_input = get_user_input()

        if user_input is None:
            break

        if not user_input.strip():
            continue

        if user_input.strip().lower() == "/status":
            print_provider_status()
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        response_text, active_model = run_agent_turn(messages)

        if response_text is None:
            print(
                "\n❌ No model currently available."
            )
            print(
                f"   Gateway: {active_model}"
            )
            print(
                "   Your conversation was kept; "
                "you can try again.\n"
            )

            messages.pop()
            continue

        messages.append({
            "role": "assistant",
            "content": response_text
        })

        try:
            exec_data = json.loads(response_text.strip())

        except json.JSONDecodeError:
            print(
                f"\n🤖 {active_model} ➔ "
                f"{response_text}\n"
            )
            continue

        if not isinstance(exec_data, dict):
            print(
                f"\n🤖 {active_model} ➔ "
                f"{response_text}\n"
            )
            continue

        if "command" not in exec_data:
            print(
                f"\n🤖 {active_model} ➔ "
                f"{response_text}\n"
            )
            continue

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

        final_reply, final_model = run_agent_turn(messages)

        if final_reply is None:
            print(
                "\n⚠️ Command executed, but no model is "
                "currently available to summarize the result.\n"
            )
            continue

        print(
            f"🤖 {final_model} ➔ "
            f"{final_reply}\n"
        )

        messages.append({
            "role": "assistant",
            "content": final_reply
        })


if __name__ == "__main__":
    main()
