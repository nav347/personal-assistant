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

        command = first_line.strip().lower()

        if command in ("exit", "quit"):
            return None

        if command == "/paste":
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


def extract_command(response_text):
    """
    The current harness uses JSON commands rather than native
    provider tool calling.

    Return parsed command data only when the entire response is
    valid JSON containing a string 'command'.
    """

    try:
        data = json.loads(response_text.strip())
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(data, dict):
        return None

    command = data.get("command")

    if not isinstance(command, str) or not command.strip():
        return None

    return data


def execute_agent_command(exec_data, active_model):
    thought = exec_data.get("thought", "")
    command = exec_data["command"]

    print(
        f"\n🧠 Agent Layer [{active_model}]: "
        f"{thought}"
    )

    print(
        f"💻 Shell Action: "
        f"{command}"
    )

    output = tools.execute_bash(command)

    stdout = output.get("stdout", "")
    stderr = output.get("stderr", "")
    code = output.get("code", 1)

    terminal_output = stdout if stdout else stderr

    print(
        f"📊 Terminal Output:\n"
        f"{terminal_output}\n"
    )

    return {
        "role": "user",
        "content": (
            f"Terminal Result (Exit Code {code}):\n"
            f"STDOUT:\n{stdout}\n"
            f"STDERR:\n{stderr}"
        )
    }


def main():
    print("🤖 PERSONAL OS AGENT ONLINE")
    print("Type 'exit' or 'quit' to close.")
    print("Type '/paste' for multiline input.")
    print()

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

        response_text, active_model = api_clients.call_llm(messages)

        if response_text is None:
            print(
                "\n⚠️ No provider was available for this request."
            )
            print(
                "The conversation remains open; try again.\n"
            )

            messages.pop()
            continue

        messages.append({
            "role": "assistant",
            "content": response_text
        })

        exec_data = extract_command(response_text)

        if exec_data is None:
            print(
                f"\n🤖 {active_model} ➔ "
                f"{response_text}\n"
            )
            continue

        terminal_message = execute_agent_command(
            exec_data,
            active_model
        )

        messages.append(terminal_message)

        final_reply, final_model = api_clients.call_llm(
            messages
        )

        if final_reply is None:
            print(
                "\n⚠️ Command completed, but no provider was "
                "available to summarize the result.\n"
            )
            continue

        messages.append({
            "role": "assistant",
            "content": final_reply
        })

        print(
            f"🤖 {final_model} ➔ "
            f"{final_reply}\n"
        )


if __name__ == "__main__":
    main()
