"""Display the contents of a stored object in the mini-git repository."""

import blob


def cat_file(object_id: str) -> None:
    """Print the type and decoded contents of the specified object."""
    obj_type, content = blob.read_object(object_id)

    print(obj_type)
    print(content.decode(errors="replace"))
