import tkinter as tk
from tkinter import font
import json

# --- Data Handling ---
def open_json_db():
    """
    Loads food and drink data from a JSON file.
    Returns the data as a Python list of dictionaries.
    """
    try:
        with open("FoodDrinks.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from 'FoodDrinks.json'. Please check the file's format.")
        return []
    except FileNotFoundError:
        print("Error: 'FoodDrinks.json' not found. Please make sure the file is in the same directory as the script.")
        return []

# --- Application Logic ---
def create_menu_items(parent_frame, food_data):
    """
    Dynamically creates and displays a card for each food item.
    """
    row, col = 0, 0
    for item in food_data:
        # Create a new Frame to serve as the "card" for each item
        item_card = tk.Frame(parent_frame, bg="#f3f4f6", relief=tk.GROOVE, borderwidth=2)
        item_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # --- Widgets inside the card ---
        # Item Name Label
        name_label = tk.Label(item_card, text=item['name'], font=('Helvetica', 14, 'bold'), bg="#f3f4f6")
        name_label.pack(pady=(10, 5))
        
        # Item Description Label
        desc_label = tk.Label(item_card, text=item['description'], font=('Helvetica', 10), wraplength=200, bg="#f3f4f6")
        desc_label.pack(padx=10)
        
        # Item Price Label
        price_label = tk.Label(item_card, text=f"RM{item['price']:.2f}", font=('Helvetica', 12, 'bold'), bg="#f3f4f6")
        price_label.pack(pady=(5, 10))
        
        # Add to Cart Button
        add_button = tk.Button(item_card, text="Add to Cart", font=('Helvetica', 10, 'bold'), bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", relief="flat")
        add_button.pack(pady=10, padx=20, fill="x")

        # Update the grid position for the next card
        col += 1
        if col > 2:  # 3 columns per row
            col = 0
            row += 1


# Main application setup
root = tk.Tk()
root.title("Cinema Food Kiosk")
root.geometry("800x600")
root.config(bg="#000033")

# Add the main title
title_label = tk.Label(root, text="Select Your Food and Drinks", font=('Helvetica', 18, 'bold'))
title_label.pack(pady=10)

# Frame to hold all the food cards
menu_frame = tk.Frame(root)
menu_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Open the JSON data and create the menu
food_data = open_json_db()
if food_data:
    create_menu_items(menu_frame, food_data)
    
root.mainloop()
