from crew import run_crew

def get_multiline_input():
    print("\nEnter your prompt (type END on a new line to finish):\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

def main():
    print("=== Autonomous Agent System ===")

    user_prompt = get_multiline_input()

    if not user_prompt.strip():
        print("❌ Empty prompt. Exiting.")
        return

    result = run_crew(user_prompt)

    print("\n=== FINAL OUTPUT ===\n")
    print(result)

if __name__ == "__main__":
    main()
