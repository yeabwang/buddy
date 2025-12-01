# Buddy - AI Coding Assistant

Buddy is a CLI tool that leverages Groq's LLMs to help you write, explain, and refactor code directly from your terminal.

## Installation

```bash
pip install buddy-ai-cli
```

Or install from source:

```bash
git clone https://github.com/yeabwang/buddy.git
cd buddy
pip install .
```

## Configuration

### 1. Set up API Key
Buddy uses Groq. You need to set your API key first.

```bash
buddy config --key <YOUR_GROQ_API_KEY>
```

### 2. Health Check & Dependencies
Run `buddy config` without arguments to check your API key status and install dependencies from a `requirements.txt` if present in your current directory.

```bash
buddy config
```

## Usage

### Generate Code
Ask a question in a text file and get the code output.

```bash
# Create a question file
echo "Write a Python script to scrape a website" > question.txt

# Generate code
buddy code question.txt -a scraper.py
```

### Explain Code
Get a clear explanation of what a code file does.

```bash
buddy explain complex_script.py
```

### Refactor Code
Refactor code to be cleaner and more efficient.

```bash
# Print refactored code to stdout
buddy refactor legacy_code.py

# Save refactored code to a file
buddy refactor legacy_code.py -o clean_code.py
```

### Options
- `-m, --model`: Specify the LLM model to use (default: `openai/gpt-oss-20b`).
  ```bash
  buddy code question.txt -a answer.py -m llama3-70b-8192
  ```

## License

MIT
