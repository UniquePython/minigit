"""Display the commit history of the current mini-git repository."""

from pathlib import Path
import commit


def log() -> None:
    """Print the commit log starting from HEAD and walking through parent commits."""
    head = Path(".minigit/HEAD").read_text().strip()
    current = head if head else None

    while current:
        data = commit.read_commit(current)

        print(f"commit {current}")
        print(f"Author: {data['author']}")
        print()
        for line in data["message"].splitlines():
            print(f"    {line}")
        print()

        current = data.get("parent")
