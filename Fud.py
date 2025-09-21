import tkinter as tk
from tkinter import font
import json

#Open Json DB for food and drinks 

def OpenJsonDB():
    try: 
        with open("FoodDrinks.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error file gone wrong")
    except FileNotFoundError:
        print("Cant find file")

root = tk.Tk()
root.mainloop()

