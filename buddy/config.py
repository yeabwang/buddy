import os
from pathlib import Path
from dotenv import load_dotenv, set_key

ENV_FILE = Path(".env")

def save_api_key(api_key):
    """Saves the API key to a .env file in the current directory."""
    if not ENV_FILE.exists():
        ENV_FILE.touch()
    
    # set_key writes the key to the .env file
    set_key(ENV_FILE, 'GROQ_API_KEY', api_key)
    print(f"API key saved to {ENV_FILE.absolute()}")

def get_api_key():
    """Retrieves the API key from the environment or .env file."""
    # Explicitly look in the current directory first
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
    else:
        # Fallback to searching parent directories
        load_dotenv()
        
    return os.getenv('GROQ_API_KEY')
