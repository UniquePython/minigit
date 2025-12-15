"""Restores the working directory to a specific commit."""

import shutil
from pathlib import Path

import blob
import tree
import commit

def checkout(commit_id: str, target_dir: Path = Path(".")) -> None:
    """
    Restore the working directory to match the given commit.

    Args:
        commit_id (str): The commit hash to checkout.
        target_dir (Path): The directory to restore files into.
    """
    # 1. Read commit to get root tree
    commit_data = commit.read_commit(commit_id)
    root_tree_id = commit_data["tree"]

    # 2. Clean target directory except .minigit
    for item in target_dir.iterdir():
        if item.name == ".minigit":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    # 3. Recursively checkout tree
    _checkout_tree(root_tree_id, target_dir)


def _checkout_tree(tree_id: str, path: Path) -> None:
    """
    Recursively restore a tree object into the given directory.

    Args:
        tree_id (str): SHA-256 hash of the tree object
        path (Path): Directory path to restore files into
    """
    path.mkdir(parents=True, exist_ok=True)

    entries = tree.read_tree(tree_id)

    for entry in entries:
        entry_path = path / entry.name

        if entry.mode == "100644":  # file
            _, content = blob.read_object(entry.object_id)
            entry_path.write_bytes(content)

        elif entry.mode == "040000":  # directory
            _checkout_tree(entry.object_id, entry_path)
