import json
import unittest
from pathlib import Path
from unittest.mock import patch

from todo_app import Task, TodoApp


class TestTodoApp(unittest.TestCase):
    def setUp(self) -> None:
        # Создаем временный файл для тестов
        self.test_file = Path("test_todo.json")

        # Отключаем GUI
        self.gui_patch = patch('customtkinter.CTk.mainloop')
        self.gui_patch.start()

        # Патчим путь к файлу в приложении (изменено)
        with patch('pathlib.Path.__file__', create=True) as mock_file:
            mock_file.parent = Path()
            self.app = TodoApp()
            self.app.data_file = self.test_file

    def tearDown(self) -> None:
        # Удаляем временный файл после тестов
        if self.test_file.exists():
            self.test_file.unlink()
        # Останавливаем патч GUI
        self.gui_patch.stop()

    def test_add_task(self) -> None:
        """Тест добавления новой задачи"""
        with patch('todo_app.TodoInputDialog') as mock_dialog:
            # Настраиваем мок диалога
            mock_dialog.return_value.get_input.return_value = "Тестовая задача"

            # Добавляем задачу
            self.app.show_new_task_dialog()

            # Проверяем, что задача добавлена
            self.assertEqual(len(self.app.tasks), 1)
            self.assertEqual(self.app.tasks[0]["text"], "Тестовая задача")

            # Проверяем, что задача сохранена в файл
            self.assertTrue(self.test_file.exists())
            with self.test_file.open(encoding="utf-8") as f:
                saved_tasks = json.load(f)
                self.assertEqual(saved_tasks[0]["text"], "Тестовая задача")

    def test_delete_task(self) -> None:
        """Тест удаления задачи"""
        # Добавляем тестовую задачу
        self.app.tasks = [Task(text="Задача для удаления")]
        self.app.selected_task = 0

        # Удаляем задачу
        self.app.delete_selected_task()

        # Проверяем, что задача удалена
        self.assertEqual(len(self.app.tasks), 0)
        self.assertIsNone(self.app.selected_task)

    def test_edit_task(self) -> None:
        """Тест редактирования задачи"""
        # Добавляем тестовую задачу
        self.app.tasks = [Task(text="Старый текст")]
        self.app.selected_task = 0

        with patch('todo_app.TodoInputDialog') as mock_dialog:
            # Настраиваем мок диалога
            mock_dialog.return_value.get_input.return_value = "Новый текст"

            # Редактируем задачу
            self.app.edit_selected_task()

            # Проверяем, что текст задачи изменился
            self.assertEqual(self.app.tasks[0]["text"], "Новый текст")

    def test_complete_task(self) -> None:
        """Тест завершения задачи"""
        # Добавляем тестовые задачи
        self.app.tasks = [Task(text="Задача 1"), Task(text="Задача 2")]
        self.app.selected_task = 0

        # Завершаем первую задачу
        self.app.complete_selected_task()

        # Проверяем, что осталась только вторая задача
        self.assertEqual(len(self.app.tasks), 1)
        self.assertEqual(self.app.tasks[0]["text"], "Задача 2")

    def test_task_navigation(self) -> None:
        """Тест навигации по задачам"""
        # Добавляем тестовые задачи
        self.app.tasks = [
            Task(text="Задача 1"),
            Task(text="Задача 2"),
            Task(text="Задача 3"),
        ]
        self.app.selected_task = 0

        # Проверяем переход к следующей задаче
        self.app.select_next_task()
        self.assertEqual(self.app.selected_task, 1)

        # Проверяем переход к предыдущей задаче
        self.app.select_prev_task()
        self.assertEqual(self.app.selected_task, 0)

        # Проверяем циклический переход в конец списка
        self.app.select_prev_task()
        self.assertEqual(self.app.selected_task, 2)

        # Проверяем циклический переход в начало списка
        self.app.select_next_task()
        self.assertEqual(self.app.selected_task, 0)

    def test_load_tasks(self) -> None:
        """Тест загрузки задач из файла"""
        # Создаем тестовый файл с задачами
        test_tasks = [{"text": "Тестовая задача"}]
        with self.test_file.open("w", encoding="utf-8") as f:
            json.dump(test_tasks, f)

        # Загружаем задачи
        loaded_tasks = self.app.load_tasks()

        # Проверяем, что задачи загружены корректно
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0]["text"], "Тестовая задача")

    def test_empty_input(self) -> None:
        """Тест обработки пустого ввода"""
        with patch('todo_app.TodoInputDialog') as mock_dialog:
            # Настраиваем мок диалога с пустым вводом
            mock_dialog.return_value.get_input.return_value = ""

            # Пытаемся добавить пустую задачу
            self.app.show_new_task_dialog()

            # Проверяем, что задача не добавлена
            self.assertEqual(len(self.app.tasks), 0)


if __name__ == "__main__":
    unittest.main()
