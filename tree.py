import TreeEntry

import blob

import os
import hashlib
from pathlib import Path

def write_tree(directory: Path) -> str:
    """Create a tree object from a directory and store it in the object database.

    Args:
        directory (Path): The directory whose contents should be written as a tree object.
    """
    if not directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory")

    entries: list[bytes] = []

    for item in sorted(directory.iterdir(), key=lambda p: p.name):
        if item.name == ".minigit":
            continue

        if item.is_file():
            object_id, data = blob.hash_bytes(item)
            blob.store_object(object_id, data)
            mode = "100644"

        elif item.is_dir():
            object_id = write_tree(item)
            mode = "040000"

        else:
            continue  # ignore special files

        entry = (
            f"{mode} {item.name}\0".encode()
            + bytes.fromhex(object_id)
        )
        entries.append(entry)

    tree_content = b"".join(entries)
    header = f"tree {len(tree_content)}\0".encode()
    store_data = header + tree_content

    tree_id = hashlib.sha256(store_data).hexdigest()
    blob.store_object(tree_id, store_data)

    return tree_id


def read_tree(object_id: str) -> list[TreeEntry.TreeEntry]:
    """Read a tree object from the object database and parse its entries.

    Args:
        object_id (str): The hash identifier of the tree object to be read.
    """
    obj_type, content = blob.read_object(object_id)

    if obj_type != "tree":
        raise ValueError("Object is not a tree")

    entries: list[TreeEntry.TreeEntry] = []
    i = 0

    while i < len(content):
        # mode
        space = content.find(b" ", i)
        mode = content[i:space].decode()
        i = space + 1

        # name
        null = content.find(b"\0", i)
        name = content[i:null].decode()
        i = null + 1

        # object id (raw bytes)
        oid_bytes = content[i:i + 32]  # SHA-256
        object_id = oid_bytes.hex()
        i += 32

        entries.append(TreeEntry.TreeEntry(mode, name, object_id))

    return entries