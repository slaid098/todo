# Simple TODO application

Simple TODO application for managing tasks with hotkeys.

## Requirements

- Python 3.9 or higher
- Windows 10/11

## Installation
1. Disable antivirus
2. Clone the repository or download the files
3. Run `setup.bat` double click
4. Follow the installer instructions

The script automatically:
- Creates a virtual environment
- Updates pip to the latest version
- Installs all dependencies
- Configures auto-start at Windows startup
- Launches the application

## Usage

### Hotkeys

- `↑/↓` - Navigation between tasks
- `Ctrl+N` - Create a new task
- `Delete` - Delete the selected task
- `Ctrl+Space` - Mark the task as completed
- `Enter` - Edit the selected task

### Особенности

- The application automatically starts at Windows startup
- All tasks are saved automatically
- Minimalistic interface
- Only keyboard control

## Project structure

- `todo_app.py` - Main application code
- `requirements.txt` - Project dependencies
- `setup.bat` - Installation script
- `test_todo_app.py` - Unit tests

## Разработка

To run tests:
```bash
# Activate the virtual environment
venv\Scripts\activate

# Run tests
python -m unittest test_todo_app.py
``` 