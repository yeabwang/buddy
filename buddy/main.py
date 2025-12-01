import argparse
import sys
import os
from buddy.config import save_api_key, get_api_key
from buddy.llm import get_answer

def main():
    parser = argparse.ArgumentParser(description="Buddy - Your AI Coding Assistant")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Config command
    config_parser = subparsers.add_parser('config', help='Configure Buddy')
    config_parser.add_argument('--key', help='Set your Groq API Key', required=True)

    # Code command
    code_parser = subparsers.add_parser('code', help='Get code answers from a question file')
    code_parser.add_argument('input_file', help='Path to the file containing the question')
    code_parser.add_argument('-a', '--answer', help='Path to the output file for the answer', required=True)

    args = parser.parse_args()

    if args.command == 'config':
        save_api_key(args.key)
        print("Configuration updated successfully.")

    elif args.command == 'code':
        api_key = get_api_key()
        if not api_key:
            print("Error: Groq API key not found. Please run 'buddy config --key <YOUR_KEY>' first.")
            sys.exit(1)

        if not os.path.exists(args.input_file):
            print(f"Error: Input file '{args.input_file}' not found.")
            print(f"Current working directory: {os.getcwd()}")
            sys.exit(1)

        try:
            with open(args.input_file, 'r') as f:
                question = f.read()
            
            print("Thinking...")
            answer = get_answer(question, api_key)

            # Clean up markdown code blocks if writing to a code file
            # This is a simple heuristic.
            if args.answer.endswith('.py') or args.answer.endswith('.js') or args.answer.endswith('.ts'):
                if answer.startswith('```') and answer.endswith('```'):
                    lines = answer.split('\n')
                    # Remove first and last lines if they are backticks
                    if lines[0].startswith('```'):
                        lines = lines[1:]
                    if lines and lines[-1].startswith('```'):
                        lines = lines[:-1]
                    answer = '\n'.join(lines)

            with open(args.answer, 'w') as f:
                f.write(answer)
            
            print(f"Answer written to {args.answer}")

        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
