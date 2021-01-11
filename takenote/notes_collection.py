from typing import Any, Dict, Tuple

from takenote.constants import NOTES_DATA_PATH
from takenote.note import Note
from takenote.ui.note.note_ui import NoteUI
from takenote.utils import read_json, write_json


class NotesCollection:

    def __init__(self):
        self._notes: Dict[str, Note] = {}
        self._uis: Dict[str, NoteUI] = {}

    @property
    def uuids(self) -> Tuple[str]:
        return self._notes.keys()

    @property
    def save_required(self) -> bool:
        return any(note.save_required for note in self._notes.values())

    def get_note(self, uuid: str) -> Note:
        return self._notes[uuid]

    def get_note_ui(self, uuid: str) -> NoteUI:
        return self._uis[uuid]

    def add_note(self, note: Note = None) -> Note:
        note = note or Note.new()
        note.set_callbacks(on_save=(lambda: self.save(NOTES_DATA_PATH)))

        # Check if note UUID is unique. UUID collisions are in no
        # way likely to happen. Still, better be safe than sorry.
        if note.uuid in self._notes:
            raise KeyError("Note with such UUID already exists in the collection.")

        self._notes[note.uuid] = note

        return note

    def set_note_ui(self, note_uuid: str, note_ui: NoteUI):
        if note_uuid not in self._notes:
            raise KeyError("Collection does not contain a note with the given UUID.")
            
        self._uis[note_uuid] = note_ui

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
        data = read_json(path)
        notes = cls.from_dict(data)
        return notes

    @classmethod
    def from_dict(cls, data: Dict) -> "NotesCollection":
        notes = cls()
        for note_data in data["notes"]:
            note = Note.from_dict(note_data)
            notes.add_note(note)

        return notes
