# Buddy - AI Coding Assistant

## Installation

```bash
pip install -e .
```

## Usage

### Configuration

First, configure your Groq API key. This will save it to a `.env` file in your current directory:

```bash
buddy config --key <YOUR_GROQ_API_KEY>
```

Alternatively, you can manually create a `.env` file with:
```
GROQ_API_KEY=<YOUR_GROQ_API_KEY>
```

### Generating Code

Create a file with your question (e.g., `question.txt`) and run:

```bash
buddy code question.txt -a answer.py
```

This will read the question from `question.txt`, query the Groq API, and save the resulting code to `answer.py`.
