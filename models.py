from typing import TypedDict, List

class Message(TypedDict):
    """Type definition for chat messages."""
    role: str
    content: str | List[dict]
