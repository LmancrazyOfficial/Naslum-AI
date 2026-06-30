from orchestrator import Orchestrator


def print_banner():
    print("=" * 60)
    print("            AI FACTORY")
    print("      Autonomous Software Engineer")
    print("=" * 60)


def main():

    print_banner()

    orchestrator = Orchestrator()

    while True:

        try:

            user_input = input("\nAI> ").strip()

            if not user_input:
                continue

            if user_input.lower() in [
                "exit",
                "quit"
            ]:
                print("Goodbye.")
                break

            orchestrator.run(user_input)

        except KeyboardInterrupt:
            print("\nInterrupted.")
            break

        except Exception as e:
            print(f"\nFatal Error: {e}")


if __name__ == "__main__":
    main()
