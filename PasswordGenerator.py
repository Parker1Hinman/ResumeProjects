import random
from tkinter import *

root = Tk()

user_input = Entry(root, width=40, borderwidth=5)
user_input.grid(row=1,column=0)

InstructionLabel = Label(text="How long should your password be?")
InstructionLabel.grid(row=0,column=0)


character_string = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()-=+_?.>,<'
length_of_string = len(character_string)

def generatePassword(length):
        password = ""
        length = int(length)
        match length:
            case _ if length > 20:
                password = "Enter a number between 1 and 15"
            case _ if length < 1:
                password = "Enter a number between 1 and 15"
            case _ if 0 < length < 21:
                for i in range(length):
                    random_index = random.randint(0,length_of_string-1)
                    password += character_string[random_index]
        
        password_label= Label(text=password)
        password_label.grid(row=3,column=0)
        return password_label 


generate_button = Button(root, padx=20, pady=10, text="Generate Password", command=lambda:generatePassword(user_input.get()))
generate_button.grid(row=2, column=0)

root.mainloop()


