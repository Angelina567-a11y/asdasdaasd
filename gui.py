import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

# Предопределённый список задач
TASKS = [
    {"task": "Прочитать статью", "type": "учёба"},
    {"task": "Сделать зарядку", "type": "спорт"},
    {"task": "Ответить на письмо", "type": "работа"},
    {"task": "Посмотреть фильм", "type": "отдых"},
    {"task": "Пойти прогуляться", "type": "отдых"},
    {"task": "Изучить новую тему", "type": "учёба"},
    {"task": "Сделать домашнюю работу", "type": "учёба"},
    {"task": "Пробежать 5 км", "type": "спорт"},
    {"task": "Выполнить проект", "type": "работа"},
]

def save_history(history):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def run_app(history):
    root = tk.Tk()
    root.title("Random Task Generator")
    root.geometry("600x500")

    # Фильтр по типу задач
    filter_var = tk.StringVar(value='Все')
    filter_options = ['Все', 'учёба', 'спорт', 'работа', 'отдых']
    ttk.Label(root, text="Фильтр по типу:").pack(pady=5)
    filter_combo = ttk.Combobox(root, textvariable=filter_var, values=filter_options, state='readonly')
    filter_combo.pack()

    # Список истории задач
    listbox = tk.Listbox(root, width=80, height=15)
    listbox.pack(pady=10)

    # Текущая задача
    current_task_var = tk.StringVar()
    ttk.Label(root, text="Текущая задача:").pack()
    task_label = ttk.Label(root, textvariable=current_task_var, font=('Arial', 14))
    task_label.pack(pady=5)

    def update_listbox():
        listbox.delete(0, tk.END)
        for item in history:
            if filter_var.get() == 'Все' or item['type'] == filter_var.get():
                listbox.insert(tk.END, f"{item['task']} ({item['type']})")
    
    def generate_task():
        filtered_tasks = [t for t in TASKS if filter_var.get() == 'Все' or t['type'] == filter_var.get()]
        if not filtered_tasks:
            messagebox.showinfo("Информация", "Нет задач для выбранного фильтра")
            return
        task = random.choice(filtered_tasks)
        current_task_var.set(f"{task['task']} ({task['type']})")
        # Добавляем в историю
        history.append(task)
        save_history(history)
        update_listbox()

    def add_task():
        task_name = new_task_entry.get().strip()
        task_type = new_type_var.get()
        if not task_name:
            messagebox.showerror("Ошибка", "Название задачи не должно быть пустым")
            return
        new_task = {"task": task_name, "type": task_type}
        TASKS.append(new_task)
        # Если фильтр совпадает — добавляем в историю
        if filter_var.get() == 'Все' or task_type == filter_var.get():
            history.append(new_task)
            save_history(history)
            update_listbox()
        new_task_entry.delete(0, tk.END)

    # Поля для добавления новой задачи
    frame_add = ttk.Frame(root)
    frame_add.pack(pady=10)
    ttk.Label(frame_add, text="Новая задача:").grid(row=0, column=0, padx=5)
    new_task_entry = ttk.Entry(frame_add, width=25)
    new_task_entry.grid(row=0, column=1, padx=5)
    new_type_var = tk.StringVar(value='учёба')
    ttk.Label(frame_add, text="Тип:").grid(row=0, column=2, padx=5)
    type_combo = ttk.Combobox(frame_add, textvariable=new_type_var, values=['учёба', 'спорт', 'работа', 'отдых'])
    type_combo.grid(row=0, column=3, padx=5)
    add_button = ttk.Button(frame_add, text="Добавить задачу", command=add_task)
    add_button.grid(row=0, column=4, padx=5)

    # Кнопка для генерации задачи
    generate_button = ttk.Button(root, text="Сгенерировать задачу", command=generate_task)
    generate_button.pack(pady=10)

    # Обновление списка при смене фильтра
    def on_filter_change(event):
        update_listbox()

    filter_combo.bind('<<ComboboxSelected>>', on_filter_change)

    # Изначально выводим историю
    update_listbox()

    root.mainloop()
