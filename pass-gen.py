import tkinter as tk
import random
import string
import sqlite3

# Function to generate a random password
def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to save the generated password to the database
def save_to_database(password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, password TEXT)")
    c.execute("INSERT INTO passwords (password) VALUES (?)", (password,))
    conn.commit()
    conn.close()

# Function to handle button click event
def generate_button_clicked():
    length = int(entry_length.get())
    password = generate_password(length)
    label_password.config(text="Generated Password: " + password)
    save_to_database(password)

# GUI setup
root = tk.Tk()
root.title("Password Generator")

label_length = tk.Label(root, text="Enter Password Length:")
label_length.pack()

entry_length = tk.Entry(root)
entry_length.pack()

generate_button = tk.Button(root, text="Generate Password", command=generate_button_clicked)
generate_button.pack()

label_password = tk.Label(root, text="")
label_password.pack()

root.mainloop()
