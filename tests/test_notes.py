import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import main


class NotesOperationsTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.notes_path = Path(self.tmp_dir.name) / "notes.txt"

        patcher = mock.patch.object(main, "NOTES_FILE", str(self.notes_path))
        patcher.start()
        self.addCleanup(patcher.stop)

    def write_notes(self, *notes):
        self.notes_path.write_text(
            "".join(f"{note}\n" for note in notes), encoding="utf-8"
        )

    def read_notes(self):
        return self.notes_path.read_text(encoding="utf-8").splitlines()

    def test_load_notes_ignores_blank_lines(self):
        self.write_notes("first", "", "second")

        self.assertEqual(main.load_notes(), ["first\n", "second\n"])

    def test_load_notes_returns_empty_list_when_file_is_missing(self):
        self.assertEqual(main.load_notes(), [])

    def test_add_note_appends_trimmed_text(self):
        self.assertEqual(main.add_note("  buy milk  "), "buy milk")
        self.assertEqual(self.read_notes(), ["buy milk"])

    def test_add_note_rejects_blank_text(self):
        with self.assertRaises(ValueError):
            main.add_note("   ")

        self.assertFalse(self.notes_path.exists())

    def test_update_note_replaces_selected_note(self):
        self.write_notes("first", "second", "third")

        previous = main.update_note(2, "updated")

        self.assertEqual(previous, "second")
        self.assertEqual(self.read_notes(), ["first", "updated", "third"])

    def test_update_note_rejects_invalid_index(self):
        self.write_notes("only note")

        for index in (0, 2):
            with self.assertRaises(IndexError):
                main.update_note(index, "text")

    def test_delete_note_removes_selected_note(self):
        self.write_notes("first", "second", "third")

        self.assertEqual(main.delete_note(1), "first")
        self.assertEqual(self.read_notes(), ["second", "third"])

    def test_delete_note_rejects_invalid_index(self):
        with self.assertRaises(IndexError):
            main.delete_note(1)

    def test_search_notes_is_case_insensitive(self):
        self.write_notes("Buy MILK", "walk the dog", "milk chocolate")

        self.assertEqual(
            main.search_notes("milk"), ["Buy MILK\n", "milk chocolate\n"]
        )

    def test_search_notes_rejects_blank_keyword(self):
        with self.assertRaises(ValueError):
            main.search_notes("  ")


if __name__ == "__main__":
    unittest.main()
