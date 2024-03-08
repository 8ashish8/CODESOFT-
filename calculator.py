from tkinter import *

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

if __name__ == "__main__":
    gui = Tk()
    gui.configure(background="lightblue")
    gui.title("Simple Calculator")
    gui.geometry("270x200")

    expression = StringVar()
    result_field = Entry(gui, textvariable=expression)
    result_field.grid(columnspan=4, ipadx=70)

    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+',
        'C', 'X', '%'
    ]

    row_val = 2
    col_val = 0

    for button in buttons:
        if button == '=':
            btn = Button(gui, text=button, fg='black', bg='dark orange', command=evaluate_expression, height=1, width=7)
        elif button == 'C':
            btn = Button(gui, text=button, fg='black', bg='yellow', command=clear_expression, height=1, width=7)
        elif button == 'X':
            btn = Button(gui, text=button, fg='black', bg='yellow', command=delete_last, height=1, width=7)
        
        else:
            btn = Button(gui, text=button, fg='black', bg='white', command=lambda b=button: update_expression(b), height=1, width=7)

        btn.grid(row=row_val, column=col_val)

        col_val += 1
        if col_val > 3:
            col_val = 0
            row_val += 1

    gui.mainloop()
