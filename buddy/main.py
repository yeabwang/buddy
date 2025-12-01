import click
import sys
import os
import subprocess
from buddy.config import save_api_key, get_api_key
from buddy.llm import get_answer

@click.group()
def main():
    """Buddy - Your AI Coding Assistant"""
    pass

@main.command()
@click.option('--key', required=False, help='Set your Groq API Key')
def config(key):
    """Configure Buddy.
    
    Without options: Checks health and installs dependencies.
    With --key: Sets the Groq API Key.
    """
    if key:
        save_api_key(key)
        click.echo("API Key updated successfully.")
        return

    click.echo("--- Buddy Health Check & Setup ---")
    
    # Check API Key
    api_key = get_api_key()
    if api_key:
        masked_key = f"...{api_key[-4:]}" if len(api_key) > 4 else "***"
        click.echo(f"✅ API Key is set ({masked_key})")
    else:
        click.echo("❌ API Key is NOT set.")
        click.echo("   Run 'buddy config --key <YOUR_KEY>' to set it.")

    # Proactively install packages if requirements.txt exists
    if os.path.exists('requirements.txt'):
        click.echo("\n📦 Found requirements.txt. Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            click.echo("✅ Dependencies installed successfully.")
        except subprocess.CalledProcessError:
            click.echo("❌ Error installing dependencies.", err=True)
    else:
        click.echo("\nℹ️ No requirements.txt found in current directory. Skipping dependency installation.")
    
    click.echo("\n----------------------------------")

def _get_api_key_or_exit():
    api_key = get_api_key()
    if not api_key:
        click.echo("Error: Groq API key not found. Please run 'buddy config --key <YOUR_KEY>' first.", err=True)
        sys.exit(1)
    return api_key

def _read_file_or_exit(file_path):
    if not os.path.exists(file_path):
        click.echo(f"Error: Input file '{file_path}' not found.", err=True)
        click.echo(f"Current working directory: {os.getcwd()}", err=True)
        sys.exit(1)
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)
        sys.exit(1)

def _clean_markdown(content, filename):
    if filename and (filename.endswith('.py') or filename.endswith('.js') or filename.endswith('.ts')):
        if content.startswith('```') and content.endswith('```'):
            lines = content.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].startswith('```'):
                lines = lines[:-1]
            return '\n'.join(lines)
    return content

@main.command()
@click.argument('input_file')
@click.option('-a', '--answer', 'answer_file', required=True, help='Path to the output file for the answer')
@click.option('-m', '--model', help='Model to use (default: openai/gpt-oss-20b)')
def code(input_file, answer_file, model):
    """Get code answers from a question file."""
    api_key = _get_api_key_or_exit()
    question = _read_file_or_exit(input_file)
    
    click.echo("Thinking...")
    try:
        answer = get_answer(question, api_key, model=model)
        answer = _clean_markdown(answer, answer_file)
        
        with open(answer_file, 'w') as f:
            f.write(answer)
        click.echo(f"Answer written to {answer_file}")
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)
        sys.exit(1)

@main.command()
@click.argument('input_file')
@click.option('-m', '--model', help='Model to use')
def explain(input_file, model):
    """Explain a code file."""
    api_key = _get_api_key_or_exit()
    file_content = _read_file_or_exit(input_file)
    
    click.echo("Thinking...")
    try:
        prompt = f"Explain the following code:\n\n{file_content}"
        system_prompt = "You are an expert code explainer. Analyze the code and provide a clear, concise explanation of what it does, how it works, and any potential issues."
        answer = get_answer(prompt, api_key, model=model, system_prompt=system_prompt)
        click.echo("\nExplanation:\n")
        click.echo(answer)
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)
        sys.exit(1)

@main.command()
@click.argument('input_file')
@click.option('-o', '--output', 'output_file', help='Path to save the refactored code (optional)')
@click.option('-m', '--model', help='Model to use')
def refactor(input_file, output_file, model):
    """Refactor a code file."""
    api_key = _get_api_key_or_exit()
    file_content = _read_file_or_exit(input_file)
    
    click.echo("Thinking...")
    try:
        prompt = f"Refactor the following code to be cleaner, more efficient, and follow best practices:\n\n{file_content}"
        system_prompt = "You are an expert software engineer. Refactor the provided code. Output ONLY the refactored code. Do not include markdown backticks or explanations unless necessary comments within the code."
        answer = get_answer(prompt, api_key, model=model, system_prompt=system_prompt)
        
        if output_file:
            answer = _clean_markdown(answer, output_file)
            with open(output_file, 'w') as f:
                f.write(answer)
            click.echo(f"Refactored code written to {output_file}")
        else:
            click.echo("\nRefactored Code:\n")
            click.echo(answer)
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
