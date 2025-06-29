# LingoGrow

**LingoGrow** is a command-line tool for learning English, Arabic vocabulary using spaced repetition, quizzes, and subtitle-based word extraction.

## Features

- **Multiple Quiz Modes:**  
  - Multiple Choice  
  - Typing  
  - Pronunciation (with speech recognition)  
  - Timed Survival Quiz  
  - Quiz by Difficulty

- **Spaced Repetition:**  
  - Review wrong answers  
  - Spaced review of words  
  - Training on old/forgotten words

- **Subtitle Batch Loader:**  
  - Extracts English words from `.srt` files and translates them to Arabic

- **Progress Tracking:**  
  - Daily goal setting and progress  
  - Achievements and stats  
  - View words to learn today

- **Database Management:**  
  - Clean duplicate words

## Requirements

- Python 3.8+
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [deep-translator](https://pypi.org/project/deep-translator/)
- [tqdm](https://pypi.org/project/tqdm/)
- [speechrecognition](https://pypi.org/project/SpeechRecognition/)
- [arabic-reshaper](https://pypi.org/project/arabic-reshaper/)
- [python-bidi](https://pypi.org/project/python-bidi/)

Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage

**Before running the project for the first time, you need to run `init.py` to initialize the database and required files:**
```sh
python init.py
```

Run the main program:
```sh
python LingoGrow.py
```

Follow the on-screen menu to select quiz modes, load subtitles, review words, and track your progress.

### Loading Subtitles

To add new words from `.srt` files:
1. Place your `.srt` files in a folder.
2. Choose option `[7] (📂) Load Multiple SRT Files` and enter the folder path.

### Setting Daily Goal

Choose option `[15] (⚙️) Change Daily Goal` to set how many words you want to learn each day.

### Cleaning Duplicates

Choose option `[8] (🧹) Clean Duplicate Words` to remove duplicate entries from your vocabulary database.

## Database

- Uses SQLite (`database/lingogrow.db`).
- Vocabulary and settings are stored persistently.

## File Structure

- `LingoGrow.py` — Main entry point and menu
- `core/` — All core modules (quizzes, models, utils, etc.)

## Troubleshooting

- Errors are logged to `lingogrow.log`.
- If you encounter issues with speech recognition, ensure your microphone is set up and try running as administrator.

## Author

- **@Petter0x1**
