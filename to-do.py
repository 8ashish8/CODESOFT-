import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

class TodoList:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY,
                            task TEXT,
                            done BOOLEAN
                          )''')
        self.conn.commit()

    def add_task(self, task):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (task, done) VALUES (?, ?)", (task, False))
        self.conn.commit()
        messagebox.showinfo("Task Added", f'Task "{task}" added to the to-do list.')

    def view_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        if not tasks:
            messagebox.showinfo("To-Do List", 'No tasks in the to-do list.')
        else:
            task_list = '\n'.join([f'{task[0]}. {task[1]} ({ "Done" if task[2] else "Pending"})' for task in tasks])
            messagebox.showinfo("To-Do List", f'To-Do List:\n{task_list}')

    def update_task_status(self, task_id, status):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tasks SET done=? WHERE id=?", (status, task_id))
        self.conn.commit()
        messagebox.showinfo("Task Updated", f'Task with ID {task_id} updated.')

    def remove_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()
        messagebox.showinfo("Task Removed", f'Task with ID {task_id} removed from the to-do list.')

# GUI
class TodoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")
        self.todo_list = TodoList("todo_list.db")

        self.label = tk.Label(master, text="To-Do List")
        self.label.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.view_button = tk.Button(master, text="View Tasks", command=self.view_tasks)
        self.view_button.pack()

        self.update_button = tk.Button(master, text="Update Task", command=self.update_task)
        self.update_button.pack()

        self.remove_button = tk.Button(master, text="Remove Task", command=self.remove_task)
        self.remove_button.pack()

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter the task:")
        if task:
            self.todo_list.add_task(task)

    def view_tasks(self):
        self.todo_list.view_tasks()

    def update_task(self):
        task_id = simpledialog.askinteger("Update Task", "Enter the task ID:")
        status = simpledialog.askstring("Update Task", "Enter the status (True/False):")
        if task_id and status:
            self.todo_list.update_task_status(task_id, status)

    def remove_task(self):
        task_id = simpledialog.askinteger("Remove Task", "Enter the task ID:")
        if task_id:
            self.todo_list.remove_task(task_id)

def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

