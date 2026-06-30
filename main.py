from orchestrator import Orchestrator

def main():
    print("AI Factory Starting...")

    orchestrator = Orchestrator()

    while True:
        user_input = input("\nEnter task (or 'exit'): ")

        if user_input.lower() == "exit":
            break

        result = orchestrator.run(user_input)
        print("\n=== RESULT ===")
        print(result)

if __name__ == "__main__":
    main()
