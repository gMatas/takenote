from string import Template
from typing import Any, Callable, Dict, NamedTuple, Optional, Tuple, Union
from uuid import uuid4

from takenote.ui.note.note_pin_mode import NotePinMode
from takenote.utils import Position, Size


class NoteStyle(NamedTuple):

    background_color: str
    font_family: str
    font_size: str
    text_color: str

    def fill_css_template(self, filepath: str) -> str:
        with open(filepath, "r") as file:
            css_template = Template(file.read())

        css_string = css_template.substitute(**self._asdict())
        return css_string

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NoteStyle":
        return cls(
            background_color=data["background_color"],
            font_family=data["font_family"],
            font_size=data["font_size"],
            text_color=data["text_color"],
        )


class Note:

    def __init__(
            self,
            uuid: str,
            content: str,
            pinmode: NotePinMode,
            style: NoteStyle,
            position: Union[Position, Tuple[Any, Any]] = None,
            size: Union[Size, Tuple[Any, Any]] = None,
            save_required: bool = False,
    ):
        self._uuid = uuid
        self._content = content
        self._pinmode = pinmode
        self._position = position
        self._size = size
        self._style = style

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
    def style(self) -> NoteStyle:
        return self._style

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

    @style.setter
    def style(self, value: NoteStyle):
        self._save_required |= self._style != value
        self._style = value

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

    def set_callbacks(self, on_save: Optional[Callable]):
        self._on_save_cb = on_save

    def save(self) -> Any:
        if self._save_required and self._on_save_cb:
            value = self._on_save_cb()
            return value

    def to_dict(self) -> Dict[str, Any]:
        note_dict = {
            "uuid": self._uuid,
            "content": self._content,
            "pinmode": self._pinmode.name,
            "style": self._style.to_dict(),
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
            style=NoteStyle.from_dict(data["style"]),
            position=_ if (_ := data["position"]) is None else Position(*_),
            size=_ if (_ := data["size"]) is None else Size(*_), 
            save_required=False
        )

        return note

    @classmethod
    def new(cls):
        # TODO Make default values not hardcoded here!
        note = cls(
            uuid=str(uuid4()),
            content="",
            pinmode=NotePinMode.NONE,
            style=NoteStyle(
                background_color="pink",
                font_family="inherit",
                font_size="inherit",
                text_color="black",
            ),
            save_required=True
        )

        return note
