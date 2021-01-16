from typing import Any, Dict, List, Optional, Tuple

from takenote.constants import NOTES_DATA_PATH
from takenote.note import Note
from takenote.ui.note.note_ui import NoteUI
from takenote.utils import read_json, write_json


class NotesCollection:

    def __init__(self):
        self._notes: Dict[str, Note] = {}
        self._uis: Dict[str, NoteUI] = {}

    @property
    def uuids(self) -> List[str]:
        return self._notes.keys()

    @property
    def save_required(self) -> bool:
        return any(note.save_required for note in self._notes.values())

    def get_note(self, uuid: str) -> Note:
        return self._notes[uuid]

    def get_note_ui(self, uuid: str) -> Optional[NoteUI]:
        return self._uis.get(uuid)

    def add_note(self, note: Note = None) -> Note:
        note = note or Note.new()
        note.set_callbacks(on_save=(lambda: self.save(NOTES_DATA_PATH)))

        # Check if note UUID is unique. UUID collisions are in no
        # way likely to happen. Still, better be safe than sorry.
        if note.uuid in self._notes:
            raise KeyError("Note with such UUID already exists in the collection.")

        self._notes[note.uuid] = note

        return note

    def set_note_ui(self, note_uuid: str, note_ui: Optional[NoteUI]):
        if note_uuid not in self._notes:
            raise KeyError("Collection does not contain a note with the given UUID.")

        if not note_ui:
            self._uis.pop(note_uuid, None)
            return

        note = self.get_note(note_uuid)
        note.position = note.position or note_ui.get_window_position()
        note.size = note.size or note_ui.get_window_size()
        self._uis[note_uuid] = note_ui

    def remove_note(self, note_uuid: str) -> Tuple[Note, NoteUI]:
        self._notes.pop(note_uuid, None)
        self._uis.pop(note_uuid, None)

    def save(self, path: str):
        if not self.save_required:
            return

        data = self.to_dict()
        write_json(path, data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "notes": [note.to_dict() for note in self._notes.values()]
        }

    @classmethod
    def load(cls, path: str) -> "NotesCollection":
        # TODO: Handle corrupted file case.
        data = read_json(path)
        notes = cls.from_dict(data)
        return notes

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NotesCollection":
        notes = cls()
        for note_data in data["notes"]:
            note = Note.from_dict(note_data)
            notes.add_note(note)

        return notes
