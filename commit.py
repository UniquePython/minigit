import time
import hashlib
from pathlib import Path

import config

import blob

def write_commit(tree_id: str, message: str, parent: str | None = None) -> str:
    """Create a commit object from a tree and message, store it, and update HEAD.

    Args:
        tree_id (str): The hash identifier of the tree object this commit points to.
        message (str): The commit message.
        parent (str | None): Optional hash of the parent commit.
    """
    lines = []
    lines.append(f"tree {tree_id}")

    if parent:
        lines.append(f"parent {parent}")

    timestamp = int(time.time())
    name, email = config.get_username()
    lines.append(f"author {name} {email} {timestamp}")
    lines.append(f"committer {name} {email} {timestamp}")
    lines.append("")  # blank line before message
    lines.append(message)

    content = "\n".join(lines).encode()

    header = f"commit {len(content)}\0".encode()
    store_data = header + content

    commit_id = hashlib.sha256(store_data).hexdigest()
    blob.store_object(commit_id, store_data)

    # update HEAD
    head_path = Path(".minigit/HEAD")
    head_path.parent.mkdir(parents=True, exist_ok=True)
    head_path.write_text(commit_id)

    return commit_id


def read_commit(commit_id: str) -> dict:
    """Read a commit object from the object database and parse its metadata and message.

    Args:
        commit_id (str): The hash identifier of the commit to read.
    """
    obj_type, content = blob.read_object(commit_id)

    if obj_type != "commit":
        raise ValueError("Object is not a commit")

    text = content.decode()
    header, message = text.split("\n\n", 1)

    data = {}
    for line in header.splitlines():
        key, value = line.split(" ", 1)
        data[key] = value

    data["message"] = message
    return data