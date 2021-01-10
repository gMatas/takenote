from uuid import uuid4
from typing import Any, Dict, Callable, Optional

from takenote.ui.note.note_pin_mode import NotePinMode


class Note:

    def __init__(
            self,  
            uuid: str,
            content: str, 
            pinmode: NotePinMode,
            save_required: bool = False, 
    ):
        self._uuid = uuid
        self._content = content
        self._pinmode = pinmode

        self._save_required = save_required
        self._on_save_cb: Optional[Callable] = None
            
    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def content(self) -> str:
        return self._content

    @property
    def pinmode(self) -> NotePinMode:
        return self._pinmode

    @property
    def save_required(self) -> bool:
        return self._save_required

    @content.setter
    def content(self, value):
        self._save_required |= self._content != value
        self._content = value

    @pinmode.setter
    def pinmode(self, value):
        self._save_required |= self._pinmode != value
        self._pinmode = value

    def save(self) -> Any:
        if self._save_required and self._on_save_cb:
            value = self._on_save_cb()
            return value

    def set_callbacks(self, on_save: Callable = None):
        self._on_save_cb = on_save

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uuid": self._uuid,
            "pinmode": self.pinmode.name,
            "content": self.content
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Note":
        note = cls(
            uuid=data["uuid"],
            content=data["content"],
            pinmode=NotePinMode[data["pinmode"]]
        )

        return note

    @classmethod
    def new(cls):
        note = cls(
            uuid=str(uuid4()),
            content="",
            pinmode=NotePinMode.NONE,
            save_required=True
        )

        return note
