from typing import Dict, Any

from takenote.constants import NOTES_DATA_PATH
from takenote.note import Note
from takenote.utils import read_json, write_json


class NotesCollection:

    def __init__(self):
        self._notes: Dict[str, Note] = {}

    @property
    def save_required(self) -> bool:
        return any(note.save_required for note in self._notes.values())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "notes": [note.to_dict() for note in self._notes.values()]
        }

    def save(self, path: str):
        if not self.save_required:
            return

        data = self.to_dict()
        write_json(path, data)

    def add_note(self, note: Note = None) -> Note:
        if not note:
            note = Note.new()
            note.set_callbacks(on_save=(lambda: self.save(NOTES_DATA_PATH)))

        # Check if note UUID is unique. UUID collisions are in no
        # way likely to happen. Still, better be safe than sorry.
        if note.uuid in self._notes:
            raise KeyError(
                "Note with such UUID already exists in the collection.")

        self._notes[note.uuid] = note

        return note

    def get_note(self, uuid: str) -> Note:
        return self._notes[uuid]

    @classmethod
    def load(cls, path: str) -> "NotesCollection":
        data = read_json(path)
        notes = cls.from_dict(data)
        return notes

    @classmethod
    def from_dict(cls, data: Dict) -> "NotesCollection":
        notes = cls()
        map(lambda note: notes.add_note(note), [
            Note.from_dict(note) 
            for note in data["notes"]
        ])

        return notes
