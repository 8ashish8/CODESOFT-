import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import sqlite3

# Create/connect to SQLite database
conn = sqlite3.connect('games.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS games
             (id INTEGER PRIMARY KEY, user_choice TEXT, computer_choice TEXT, result TEXT)''')

def show_instructions():
    messagebox.showinfo("Instructions", "Welcome to Rock Paper Scissors!\n\n"
                        "Instructions:\n"
                        "1. Click on one of the buttons to choose rock, paper, or scissors.\n"
                        "2. The computer will randomly select its choice.\n"
                        "3. The winner will be determined based on the game rules.\n"
                        "4. Click 'OK' to dismiss this message and start playing!")

def show_feedback():
    feedback = simpledialog.askstring("Feedback", "We'd love to hear your feedback! Please leave your comments below:")
    if feedback:
        messagebox.showinfo("Thank You!", "Thank you for your feedback!")

def play_game(user_choice):
    global user_score, games_played
    computer_choice = random.choice(["rock", "paper", "scissors"])
    result = determine_winner(user_choice, computer_choice)
    display_result(user_choice, computer_choice, result)
    save_game(user_choice, computer_choice, result)
    update_score(result)

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        return "You win!"
    else:
        return "You lose!"

def display_result(user_choice, computer_choice, result):
    result_label.config(text=f"Your choice: {user_choice}\nComputer's choice: {computer_choice}\nResult: {result}")

def save_game(user_choice, computer_choice, result):
    c.execute("INSERT INTO games (user_choice, computer_choice, result) VALUES (?, ?, ?)",
              (user_choice, computer_choice, result))
    conn.commit()

def update_score(result):
    global user_score, games_played
    games_played += 1
    if result == "You win!":
        user_score += 1
    score_label.config(text=f"Score: {user_score}/{games_played}")

# Create the main window
root = tk.Tk()
root.title("Rock Paper Scissors Game")

# Initialize global variables for score and games played
user_score = 0
games_played = 0

# Create UI elements
instruction_button = tk.Button(root, text="Instructions", command=show_instructions)
instruction_button.pack()

feedback_button = tk.Button(root, text="Feedback", command=show_feedback)
feedback_button.pack()

instruction_label = tk.Label(root, text="Choose rock, paper, or scissors:")
instruction_label.pack()

rock_button = tk.Button(root, text="Rock", command=lambda: play_game("rock"))
rock_button.pack()

paper_button = tk.Button(root, text="Paper", command=lambda: play_game("paper"))
paper_button.pack()

scissors_button = tk.Button(root, text="Scissors", command=lambda: play_game("scissors"))
scissors_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

score_label = tk.Label(root, text="Score: 0/0")
score_label.pack()

# Run the main event loop
root.mainloop()

# Close the database connection
conn.close()
