"""Dataclass representing a tree entry (file or directory)."""

from dataclasses import dataclass

@dataclass
class TreeEntry:
    mode: str
    name: str
    object_id: str
