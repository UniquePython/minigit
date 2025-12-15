import hashlib

from pathlib import Path

def hash_bytes(input_file: Path) -> tuple[str, bytes]:
    """This function takes a file and hashes its contents.

    Args:
        input_filepath (Path): This is the path to the file whose contents should be hashed.
    """
    if not input_file.is_file():
        raise FileNotFoundError(f"No file at the location '{input_file}' was found.")
    
    content = input_file.read_bytes()
    header = f"blob {len(content)}\0".encode()
    store_data = header + content
    
    hexdigest = hashlib.sha256(store_data).hexdigest()
    
    return hexdigest, store_data


def store_object(object_id: str, data: bytes) -> None:
    """This function stores a hashed file in an object directory using the hash as the filename.

    Args:
        object_id (str): The hash of the file.
        data (bytes): The data to be stored.
    """
    base_dir = Path('.minigit/objects')
    sub_dir = base_dir / object_id[:2]
    sub_dir.mkdir(parents=True, exist_ok=True)

    file_path = sub_dir / object_id[2:]

    if not file_path.exists():
        file_path.write_bytes(data)


def read_object(object_id: str) -> tuple[str, bytes]:
    """This function reads a stored object from the object directory and reconstructs its contents.

    Args:
        object_id (str): The hash identifier of the object to be read.
    """
    base_dir = Path('.minigit/objects')
    object_path = base_dir / object_id[:2] / object_id[2:]
    
    if not object_path.exists():
        raise FileNotFoundError(f"No blob found at {object_path}")
    
    raw = object_path.read_bytes()
    header, content = raw.split(b"\0", 1)
    
    header_text = header.decode()
    obj_type, size_str = header_text.split(" ")
    size = int(size_str)
    
    if size != len(content):
        raise ValueError(f"Corrupt object: Expected size = {size} but received {len(content)}")
    
    if hashlib.sha256(raw).hexdigest() != object_id:
        raise ValueError("Object hash mismatch")
    
    return obj_type, content