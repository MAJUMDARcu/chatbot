import os
import sys

from chatbot import RetrievalChatbot


def main():
    args = sys.argv[1:]
    debug = "--debug" in args
    args = [a for a in args if a != "--debug"]

    kb_path = args[0] if args else os.path.join(
        os.path.dirname(__file__), "knowledge_base.json"
    )

    bot = RetrievalChatbot(kb_path)

    print(f"=== {bot.topic} ===")
    print("Type 'quit' to exit.\n")
    print(bot.responses.get("greeting", "Hi! Ask me something."))

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Bye!")
            break

        if not user_input:
            continue

        if bot.is_exit(user_input):
            print("Bot:", bot.responses.get("goodbye", "Bye!"))
            break

        response, info = bot.get_response(user_input)
        print("Bot:", response)
        if debug:
            print(
                f"    [debug] tag={info['tag']} "
                f"score={info['score']} "
                f"pattern={info['pattern']!r}"
            )


if __name__ == "__main__":
    main()