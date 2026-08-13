"""
Simple AI Chatbot — Terminal Version
--------------------------------------
Project 1 of the "AI Projects for Beginners" series.

What this teaches you:
  1. How to call an AI model through an API
  2. How to give the AI "memory" (conversation history) using
     Google's server-side interaction chaining
  3. How to give the AI a personality/instructions (system prompt)
  4. Basic UX for a command-line tool (colors, exit command, error handling)

HOW TO RUN:
  1. Install the one dependency:
       pip install google-genai --break-system-packages
  2. Get a free API key: https://aistudio.google.com/apikey
  3. Set it as an environment variable, OR just run the script —
     it will ask you to paste the key the first time.
       (Mac/Linux)  export GEMINI_API_KEY="your-key-here"
       (Windows)    setx GEMINI_API_KEY "your-key-here"
  4. Run it:
       python chatbot.py
"""

import os
import sys

try:
    from google import genai
except ImportError:
    print("Missing dependency. Run this first:\n")
    print("  pip install google-genai --break-system-packages\n")
    sys.exit(1)

# ---- Terminal colors (just for nicer UX, no real magic here) ----
class Color:
    USER = "\033[96m"    # cyan
    BOT = "\033[92m"      # green
    SYSTEM = "\033[93m"   # yellow
    RESET = "\033[0m"
    BOLD = "\033[1m"

MODEL = "gemini-3.5-flash-lite"  # fastest model — swap to "gemini-3.6-flash" for smarter but slower replies


def get_api_key() -> str:
    """Get the API key from an environment variable, or ask for it."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    print(f"{Color.SYSTEM}No GEMINI_API_KEY environment variable found.{Color.RESET}")
    key = input("Paste your Gemini API key here: ").strip()
    if not key:
        print("No key provided. Exiting.")
        sys.exit(1)
    return key


# ---- The chatbot's personality / instructions ----
# This is called a "system prompt". Change this text to give your bot
# a different personality, role, or set of rules.
SYSTEM_PROMPT = (
    "You are a friendly, helpful assistant chatting with a beginner who is "
    "learning to build AI projects. Keep answers clear and not too long, "
    "unless the user asks for detail."
)


def main():
    print(f"{Color.BOLD}=== AI Chatbot (Terminal Edition) ==={Color.RESET}")
    print("Type your message and press Enter.")
    print("Type 'exit' or 'quit' to stop, or 'clear' to reset memory.\n")

    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    # This holds the ID of the last turn. Google's servers keep the
    # actual conversation history for us — we just pass this ID back
    # each time to say "continue from here". That's the "memory".
    previous_interaction_id = None

    while True:
        try:
            user_input = input(f"{Color.USER}You: {Color.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            previous_interaction_id = None
            print(f"{Color.SYSTEM}(memory cleared){Color.RESET}\n")
            continue

        try:
            interaction = client.interactions.create(
                model=MODEL,
                input=user_input,
                system_instruction=SYSTEM_PROMPT,
                previous_interaction_id=previous_interaction_id,
            )
            print(f"{Color.BOT}Bot: {Color.RESET}{interaction.output_text}\n")
            previous_interaction_id = interaction.id
        except Exception as e:
            print(f"{Color.SYSTEM}Error talking to the API: {e}{Color.RESET}\n")


if __name__ == "__main__":
    main()
