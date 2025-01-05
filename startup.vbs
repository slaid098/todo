Set WshShell = CreateObject("WScript.Shell")
strPath = WshShell.CurrentDirectory
WshShell.Run "pythonw.exe " & strPath & "\todo_app.py", 0, False 