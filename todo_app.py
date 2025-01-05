import json
from pathlib import Path
from typing import Any, TypedDict

import customtkinter as ctk


class Task(TypedDict):
    text: str


class TodoInputDialog(ctk.CTkInputDialog):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.bind("<Escape>", lambda e: self.cancel())  # noqa: ARG005
        self.bind("<Return>", lambda e: self.destroy())  # noqa: ARG005

    def cancel(self) -> None:
        self.master.focus_force()
        self.destroy()


class TodoApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        # Настройка окна
        self.title("Todo")
        self.geometry("300x400")
        self.attributes("-topmost", True)  # noqa: FBT003

        # Установка темы
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Путь к файлу с задачами (изменено)
        self.data_file = Path(__file__).parent / "todo_data.json"

        # Список задач
        self.tasks = self.load_tasks()

        # Выбранная задача
        self.selected_task: int | None = None

        # Флаг для предотвращения открытия нескольких диалогов
        self.dialog_open = False

        # Создание виджетов
        self.setup_ui()

        # Привязка горячих клавиш
        self.bind("<Control-n>", lambda e: self.show_new_task_dialog())  # noqa: ARG005
        self.bind("<Control-N>", lambda e: self.show_new_task_dialog())  # noqa: ARG005
        self.bind("<Control-space>", lambda e: self.complete_selected_task())  # noqa: ARG005
        self.bind("<Delete>", lambda e: self.delete_selected_task())  # noqa: ARG005
        self.bind("<Up>", lambda e: self.select_prev_task())  # noqa: ARG005
        self.bind("<Down>", lambda e: self.select_next_task())  # noqa: ARG005
        self.bind("<Return>", lambda e: self.edit_selected_task())  # noqa: ARG005

        if self.tasks:
            self.select_task(0)

        # Фокус на главное окно для работы клавиатуры
        self.focus_force()

    def setup_ui(self) -> None:
        # Фрейм для списка задач
        self.tasks_frame = ctk.CTkScrollableFrame(self, width=280)
        self.tasks_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Информация о горячих клавишах
        info_text = (
            "Hot keys:\n"
            "UP/DOWN - Navigation between tasks\n"
            "Ctrl+N - New task\n"
            "Delete - Delete task\n"
            "Ctrl+Space - Mark as completed\n"
            "Enter - Edit task"
        )
        info_label = ctk.CTkLabel(self, text=info_text, justify="left")
        info_label.pack(pady=10, padx=10)

        self.refresh_tasks_ui()

    def load_tasks(self) -> list[Task]:
        if self.data_file.exists():
            with self.data_file.open(encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_tasks(self) -> None:
        with self.data_file.open("w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def refresh_tasks_ui(self) -> None:
        # Очистка текущего списка
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        # Создание новых виджетов для задач
        for i, task in enumerate(self.tasks):
            task_frame = ctk.CTkFrame(self.tasks_frame)
            task_frame.pack(fill="x", pady=2)

            # Добавляем номер задачи для удобства
            number_label = ctk.CTkLabel(task_frame, text=f"{i + 1}.", width=30)
            number_label.pack(side="left", padx=(5, 0))

            label = ctk.CTkLabel(task_frame, text=task["text"])
            label.pack(side="left", padx=5, fill="x", expand=True)

            # Если это выбранная задача, выделяем её
            if i == self.selected_task:
                task_frame.configure(fg_color=("gray76", "gray27"))

    def select_task(self, index: int) -> None:
        if 0 <= index < len(self.tasks):
            self.selected_task = index
            self.refresh_tasks_ui()

    def select_next_task(self) -> None:
        if self.selected_task is not None and self.tasks:
            self.select_task((self.selected_task + 1) % len(self.tasks))
        elif self.tasks:
            self.select_task(0)

    def select_prev_task(self) -> None:
        if self.selected_task is not None and self.tasks:
            self.select_task((self.selected_task - 1) % len(self.tasks))
        elif self.tasks:
            self.select_task(len(self.tasks) - 1)

    def show_new_task_dialog(self) -> None:
        if self.dialog_open:
            return

        self.dialog_open = True
        dialog = TodoInputDialog(
            text="Input new task:",
            title="New task",
        )
        task_text = dialog.get_input()
        self.dialog_open = False

        if task_text:
            self.tasks.append({"text": task_text})
            self.save_tasks()
            if len(self.tasks) == 1:  # Если это первая задача
                self.select_task(0)
            self.refresh_tasks_ui()
        self.focus_force()

    def edit_selected_task(self) -> None:
        if self.selected_task is not None and not self.dialog_open:
            self.dialog_open = True
            current_text = self.tasks[self.selected_task]["text"]
            dialog = TodoInputDialog(
                text=f"Edit task:\n{current_text}",
                title="Editing",
            )
            new_text = dialog.get_input()
            self.dialog_open = False

            if new_text:
                self.tasks[self.selected_task]["text"] = new_text
                self.save_tasks()
                self.refresh_tasks_ui()
        self.focus_force()

    def delete_selected_task(self) -> None:
        if self.selected_task is not None:
            self.tasks.pop(self.selected_task)
            self.save_tasks()

            # Обновляем выбранную задачу
            if not self.tasks:
                self.selected_task = None
            else:
                # Если удалили последнюю задачу, выбираем предыдущую
                self.selected_task = min(
                    self.selected_task,
                    len(self.tasks) - 1,
                )

            self.refresh_tasks_ui()
            self.focus_force()  # Возвращаем фокус на окно

    def complete_selected_task(self) -> None:
        if self.selected_task is not None:
            self.tasks.pop(self.selected_task)
            self.save_tasks()

            # Обновляем выбранную задачу
            if not self.tasks:
                self.selected_task = None
            else:
                # Если завершили последнюю задачу, выбираем предыдущую
                self.selected_task = min(
                    self.selected_task,
                    len(self.tasks) - 1,
                )

            self.refresh_tasks_ui()
            self.focus_force()  # Возвращаем фокус на окно


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
