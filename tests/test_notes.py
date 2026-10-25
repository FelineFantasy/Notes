import io
import json
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

    def test_parse_tags_returns_unique_lowercase_tags(self):
        self.assertEqual(
            main.parse_tags("Buy #Milk and #milk #Work-2026"),
            ["milk", "work-2026"],
        )

    def test_filter_by_tag_matches_only_tagged_notes(self):
        self.write_notes("buy #milk", "walk dog #pets", "milk chocolate")

        self.assertEqual(main.filter_by_tag("#MILK"), ["buy #milk\n"])

    def test_filter_by_tag_rejects_blank_tag(self):
        with self.assertRaises(ValueError):
            main.filter_by_tag(" # ")

    def test_export_notes_writes_json(self):
        self.write_notes("first #work", "second")
        export_path = Path(self.tmp_dir.name) / "notes.json"

        self.assertEqual(main.export_notes(export_path), 2)
        self.assertEqual(
            json.loads(export_path.read_text(encoding="utf-8")),
            [
                {"id": 1, "text": "first #work", "tags": ["work"]},
                {"id": 2, "text": "second", "tags": []},
            ],
        )

    def test_export_notes_writes_empty_list(self):
        export_path = Path(self.tmp_dir.name) / "notes.json"

        self.assertEqual(main.export_notes(export_path), 0)
        self.assertEqual(
            json.loads(export_path.read_text(encoding="utf-8")), []
        )

    def run_cli(self, *args):
        with mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
            code = main.run_cli(main.build_parser().parse_args(args))
        return code, stdout.getvalue()

    def test_cli_add_and_list(self):
        code, output = self.run_cli("--add", "from cli")

        self.assertEqual(code, 0)
        self.assertIn("Заметка добавлена!", output)
        self.assertEqual(self.read_notes(), ["from cli"])

        code, output = self.run_cli("--list")
        self.assertEqual(code, 0)
        self.assertIn("1. from cli", output)

    def test_cli_search_shows_only_matches(self):
        self.write_notes("buy milk", "walk the dog")

        code, output = self.run_cli("--search", "MILK")

        self.assertEqual(code, 0)
        self.assertIn("1. buy milk", output)
        self.assertNotIn("walk the dog", output)

    def test_cli_tag_shows_only_tagged_notes(self):
        self.write_notes("buy #milk", "walk dog #pets")

        code, output = self.run_cli("--tag", "#PETS")

        self.assertEqual(code, 0)
        self.assertIn("walk dog #pets", output)
        self.assertNotIn("buy #milk", output)

    def test_cli_delete_removes_note(self):
        self.write_notes("first", "second")

        code, output = self.run_cli("--delete", "1")

        self.assertEqual(code, 0)
        self.assertIn("first", output)
        self.assertEqual(self.read_notes(), ["second"])

    def test_cli_export_writes_file(self):
        self.write_notes("first")
        export_path = Path(self.tmp_dir.name) / "notes.json"

        code, output = self.run_cli("--export", str(export_path))

        self.assertEqual(code, 0)
        self.assertIn("1", output)
        self.assertTrue(export_path.exists())

    def test_cli_returns_error_for_invalid_number(self):
        with mock.patch("sys.stderr", new_callable=io.StringIO) as stderr:
            code = main.run_cli(
                main.build_parser().parse_args(["--delete", "5"])
            )

        self.assertEqual(code, 1)
        self.assertIn("Ошибка", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
