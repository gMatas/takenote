from typing import Any, Callable, Dict, Optional, Tuple, Union
from uuid import uuid4

from takenote.ui.note.note_pin_mode import NotePinMode
from takenote.utils import Position, Size


class Note:

    def __init__(
            self,
            uuid: str,
            content: str,
            pinmode: NotePinMode,
            position: Union[Position, Tuple[Any, Any]] = None,
            size: Union[Size, Tuple[Any, Any]] = None,
            save_required: bool = False, 
    ):
        self._uuid = uuid
        self._content = content
        self._pinmode = pinmode
        self._position = position
        self._size = size

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
    def position(self) -> Optional[Position]:
        return self._position

    @property
    def size(self) -> Optional[Size]:
        return self._size

    @property
    def save_required(self) -> bool:
        return self._save_required

    @content.setter
    def content(self, value: str):
        self._save_required |= self._content != value
        self._content = value

    @pinmode.setter
    def pinmode(self, value: NotePinMode):
        self._save_required |= self._pinmode != value
        self._pinmode = value

    @position.setter
    def position(self, value: Position):
        self._save_required |= self._position != value
        self._position = value

    @size.setter
    def size(self, value: Size):
        self._save_required |= self._size != value
        self._size = value

    def set_position(self, x: int, y: int):
        new_position = Position(x, y)
        if is_changed := self._position != new_position:
            self._position = new_position

        self._save_required |= is_changed

    def set_size(self, width: int, height: int):
        new_size = Size(width, height)
        if is_changed := self._size != new_size:
            self._size = new_size

        self._save_required |= is_changed

    def save(self) -> Any:
        if self._save_required and self._on_save_cb:
            value = self._on_save_cb()
            return value

    def set_callbacks(self, on_save: Optional[Callable]):
        self._on_save_cb = on_save

    def to_dict(self) -> Dict[str, Any]:
        note_dict = {
            "uuid": self._uuid,
            "pinmode": self._pinmode.name,
            "content": self._content,
            "position": None if self._position is None else tuple(self._position),
            "size": None if self._size is None else tuple(self._size)
        }

        return note_dict

    @classmethod
    def from_dict(cls, data: Dict) -> "Note":        
        note = cls(
            uuid=data["uuid"],
            content=data["content"],
            pinmode=NotePinMode[data["pinmode"]],
            position=_ if (_ := data["position"]) is None else Position(*_),
            size=_ if (_ := data["size"]) is None else Size(*_), 
            save_required=False
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
