from tkinter import *
import math

result = ""
history = []

def update_expression(value):
    global result
    result += str(value)
    expression.set(result)

def evaluate_expression():
    try:
        global result
        total = str(eval(result))
        history.append(f"{result} = {total}")
        expression.set(total)
        result = ""
    except:
        expression.set("Error")
        result = ""

def clear_expression():
    global result
    result = ""
    expression.set("")

def delete_last():
    global result
    result = result[:-1]
    expression.set(result)

def calculate_percentage():
    try:
        global result
        result = str(eval(result) / 100)
        expression.set(result)
    except:
        expression.set("Error")
        result = ""

def show_history():
    history_window = Toplevel(gui)
    history_window.title("History")
    history_label = Label(history_window, text='\n'.join(history))
    history_label.pack()

def add_trigonometric_function(func):
    global result
    result += func + "("
    expression.set(result)

if __name__ == "__main__":
    gui = Tk()
    gui.configure(background="lightblue")
    gui.title("Scientific Calculator")
    gui.geometry("370x300")

    expression = StringVar()
    result_field = Entry(gui, textvariable=expression)
    result_field.grid(row=0, column=0, columnspan=6, ipadx=100, pady=5)

    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+',
        '%', 'C', '<-',
        'History',
        'sin', 'cos', 'tan',
        '(', ')','rad', 'deg',
        'log', 'inv'
    ]

    row_val = 1
    col_val = 0

    for button in buttons:
        if button in ('=', 'C', '<-', 'History'):
            btn = Button(gui, text=button, fg='black', bg='dark orange', command=evaluate_expression if button == '=' else (
                clear_expression if button == 'C' else (
                    delete_last if button == '<-' else show_history
                )
            ), height=2, width=7)
        elif button in ('sin', 'cos', 'tan', '(', ')', 'rad', 'deg', 'log', 'inv'):
            btn = Button(gui, text=button, fg='black', bg='white', command=lambda b=button: add_trigonometric_function(b), height=2, width=7)
        elif button in ('/', '*', '-', '+', '%'):
            btn = Button(gui, text=button, fg='black', bg='blue', command=lambda b=button: update_expression(b), height=2, width=7)
        else:
            btn = Button(gui, text=button, fg='black', bg='white', command=lambda b=button: update_expression(b), height=2, width=7)

        btn.grid(row=row_val, column=col_val)

        col_val += 1
        if col_val > 5:
            col_val = 0
            row_val += 1

    gui.mainloop()
