import tkinter as tk
import sqlite3
from tkinter import messagebox

class ContactBookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Contact Book")

        # Connect to SQLite database
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()

        # Create contacts table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                            (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, address TEXT)''')
        self.conn.commit()

        # Labels
        tk.Label(master, text="Name:").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="Phone Number:").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="Email:").grid(row=2, column=0, sticky="e")
        tk.Label(master, text="Address:").grid(row=3, column=0, sticky="e")

        # Entries
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)
        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=1, column=1)
        self.email_entry = tk.Entry(master)
        self.email_entry.grid(row=2, column=1)
        self.address_entry = tk.Entry(master)
        self.address_entry.grid(row=3, column=1)

        # Buttons
        tk.Button(master, text="Add Contact", command=self.add_contact).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(master, text="View Contact List", command=self.view_contact_list).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Search Contact", command=self.search_contact).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Update Contact", command=self.update_contact).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Delete Contact", command=self.delete_contact).grid(row=8, column=0, columnspan=2, pady=10)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            self.cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", (name, phone, email, address))
            self.conn.commit()
            messagebox.showinfo("Success", "Contact added successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Name and Phone Number are required fields.")

    def view_contact_list(self):
        self.cursor.execute("SELECT name, phone FROM contacts")
        contacts = self.cursor.fetchall()
        if contacts:
            contact_list = "\n".join([f"{contact[0]}: {contact[1]}" for contact in contacts])
            messagebox.showinfo("Contact List", contact_list)
        else:
            messagebox.showinfo("Contact List", "No contacts found.")

    def search_contact(self):
        search_term = self.name_entry.get() or self.phone_entry.get()
        if search_term:
            self.cursor.execute("SELECT name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?", ('%'+search_term+'%', '%'+search_term+'%'))
            found_contacts = self.cursor.fetchall()
            if found_contacts:
                contact_list = "\n".join([f"{contact[0]}: {contact[1]}" for contact in found_contacts])
                messagebox.showinfo("Search Results", contact_list)
            else:
                messagebox.showinfo("Search Results", "No matching contacts found.")
        else:
            messagebox.showerror("Error", "Please enter a name or phone number to search.")

    def update_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            self.cursor.execute("UPDATE contacts SET phone=?, email=?, address=? WHERE name=?", (phone, email, address, name))
            self.conn.commit()
            messagebox.showinfo("Success", "Contact updated successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Name and Phone Number are required fields.")

    def delete_contact(self):
        name = self.name_entry.get()
        if name:
            self.cursor.execute("DELETE FROM contacts WHERE name=?", (name,))
            self.conn.commit()
            messagebox.showinfo("Success", "Contact deleted successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please enter a name to delete.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
