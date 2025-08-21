from dotenv import load_dotenv
import os

def load_env():
    load_dotenv(override=True)

def get_key(key):
    load_env()
    value = os.getenv(key)
    if value is None:
        raise KeyError(f"Environment variable '{key}' not found.")
    return value