# Notes 📝

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A console-based note manager in Python. Add, update, delete, search, tag, and export your notes.

## 📝 Description

**Notes** is a minimalist console note manager. Everything is stored locally in `notes.txt`, with numbering generated "on the fly" that remains consistent even after deletions.

### Features

- **Add** notes
- **Update** existing notes
- **Delete** notes by number
- **View** all notes with numbering
- **Search** notes by keyword (case-insensitive)
- **Tag** notes with `#hashtags` and filter by tag
- **Export** notes to JSON
- **CLI mode** for scripting and quick one-off commands

## ⚙️ Installation

```bash
git clone https://github.com/FelineFantasy/Notes
cd Notes
python main.py
```

No third-party dependencies are required.

## 🎮 Interactive Mode

Run the app without arguments to open the menu:

```bash
python main.py
```

```text
1. Add a note
2. Update a note
3. Delete a note
4. View notes
5. Search notes
6. Search notes by tag
7. Export notes to JSON
0. Exit
```

## 🖥 Command-Line Mode

Pass arguments to skip the menu and run a single command:

```bash
python main.py --add "Buy milk #shopping"
python main.py --list
python main.py --search milk
python main.py --tag shopping
python main.py --delete 1
python main.py --export notes.json
```

| Option | Description |
| --- | --- |
| `--add TEXT` | Append a note |
| `--list` | Show all notes |
| `--search WORD` | Find notes containing the word |
| `--tag TAG` | Find notes with the tag |
| `--delete NUMBER` | Delete a note by one-based number |
| `--export FILE` | Write all notes to a JSON file |

## 🏷 Tags

Any word starting with `#` is treated as a tag. Tags are case-insensitive and may contain letters, digits, underscores, and hyphens:

```text
Buy milk #shopping #home
Finish the report #work-2026
```

`--tag shopping` and `--tag "#SHOPPING"` both match the first note.

## 📤 JSON Export

Menu option 7 or `--export notes.json` writes:

```json
[
  {
    "id": 1,
    "text": "Buy milk #shopping",
    "tags": ["shopping"]
  }
]
```

## 🧪 Tests

The test suite uses only the standard library:

```bash
python -m unittest
```

## 📁 Project Files

```text
Notes/
├── main.py               # Application
├── tests/
│   └── test_notes.py     # Unit tests
├── notes.txt             # Notes file (created automatically)
├── .gitignore            # Git ignore rules
├── README.md             # Documentation
└── .github/
    └── FUNDING.yml       # GitHub funding configuration
```

## 💖 Support the Project

If you enjoy Notes and want to help keep the project alive, you can support me here:

[![DonationAlerts](https://img.shields.io/badge/DonationAlerts-Support-blue.svg)](https://www.donationalerts.com/r/felinefantasy)

Your support helps me:

- 📝 Keep improving the app
- 🐱 Develop more open-source projects
- ☕ Stay awake while coding at 4 AM

Every little bit is appreciated! ❤️

## 👤 Author
- **FelineFantasy**
- **License**: MIT
