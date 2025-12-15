"""Reads username/email configuration."""

from configparser import ConfigParser
from pathlib import Path

def get_username() -> tuple[str, str]:
    """Retrieve the username and email from the mini-git configuration.

    Reads the `.minigit/config` file and returns the configured name and email.
    If the file or values are missing, returns default values ("null", "null").
    """
    config_path = Path(".minigit/config")
    if not config_path.exists():
        return "null", "null"
    parser = ConfigParser()
    parser.read(config_path)
    name = parser["minigit"].get("name", "null")
    email = parser["minigit"].get("email", "null")
    return name, email
