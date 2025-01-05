@echo off
setlocal EnableDelayedExpansion

echo Проверка Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не установлен!
    echo Пожалуйста, установите Python 3.9 или выше с python.org
    pause
    exit /b 1
)

echo Создание виртуального окружения...
python -m venv venv
if errorlevel 1 (
    echo Ошибка при создании виртуального окружения!
    pause
    exit /b 1
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Ошибка при активации виртуального окружения!
    pause
    exit /b 1
)

echo Обновление pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Ошибка при обновлении pip!
    pause
    exit /b 1
)

echo Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo Ошибка при установке зависимостей!
    pause
    exit /b 1
)

echo Проверка установки...
python -c "import customtkinter, packaging" > nul 2>&1
if errorlevel 1 (
    echo Ошибка: Не все зависимости установлены корректно!
    pause
    exit /b 1
)

echo Настройка автозапуска...
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\todo.vbs"
echo sPath = CreateObject("WScript.Shell").CurrentDirectory >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\todo.vbs"
echo oWS.Run """%~dp0venv\Scripts\pythonw.exe"" ""%~dp0todo_app.py""", 0, False >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\todo.vbs"

echo.
echo Установка успешно завершена!
echo Приложение будет запускаться при старте Windows.
echo.
echo Для запуска прямо сейчас нажмите любую клавишу...
pause

start "" "%~dp0venv\Scripts\pythonw.exe" "%~dp0todo_app.py" 