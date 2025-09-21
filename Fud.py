import tkinter as tk
from tkinter import font
import json

#Main Vars
MainBG = "#111827"
MainFG = "#ffffff"
CardBG = "#1f2937"

# This list will act as our shopping cart
cart_items = []

# --- Data Handling ---
def open_json_db():
    """
    Loads food and drink data from a JSON file.
    Returns the data as a Python list of dictionaries.
    """
    try:
        # We use utf-8 encoding to prevent errors with special characters
        with open("FoodDrinks.json", "r", encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from 'FoodDrinks.json'. Please check the file's format.")
        return []
    except FileNotFoundError:
        print("Error: 'FoodDrinks.json' not found. Please make sure the file is in the same directory as the script.")
        return []

# --- Application Logic ---
def update_cart_display():
    """
    Clears the current cart display and rebuilds it based on the cart_items list,
    stacking duplicate items and showing the total price.
    """
    # Clear all existing widgets in the cart frame, except for the title
    for widget in cart_frame.winfo_children():
        if widget is not cart_title_label:
            widget.destroy()

    # Create a dictionary to count unique items
    item_counts = {}
    total_price = 0.0
    for item in cart_items:
        item_name = item['name']
        if item_name in item_counts:
            item_counts[item_name]['quantity'] += 1
        else:
            item_counts[item_name] = {'quantity': 1, 'price': item['price']}
        total_price += item['price']

    # Create new labels for each unique item in the cart
    row_count = 1
    for item_name, data in item_counts.items():
        quantity = data['quantity']
        price = data['price']
        subtotal = quantity * price
        
        # Frame for each cart item to hold label and remove button
        cart_item_frame = tk.Frame(cart_frame, bg="#2d3748")
        cart_item_frame.grid(row=row_count, column=0, sticky="ew", padx=10, pady=5)
        cart_item_frame.grid_columnconfigure(0, weight=1)

        cart_item_label = tk.Label(
            cart_item_frame, 
            text=f"{item_name} x{quantity} - RM{subtotal:.2f}",
            font=('Helvetica', 12), 
            bg="#2d3748", 
            fg=MainFG,
            anchor="w"
        )
        cart_item_label.grid(row=0, column=0, sticky="ew")

        # Remove item button
        remove_button = tk.Button(
            cart_item_frame,
            text="X",
            font=('Helvetica', 10, 'bold'),
            bg="#dc2626",
            fg="white",
            activebackground="#991b1b",
            activeforeground="white",
            relief="flat",
            command=lambda name=item_name: remove_from_cart(name)
        )
        remove_button.grid(row=0, column=1, sticky="e", padx=5)

        row_count += 1
    
    # Add a separator and total price label
    if cart_items:
        separator = tk.Frame(cart_frame, height=2, bg=MainFG)
        separator.grid(row=row_count, column=0, sticky="ew", padx=10, pady=5)
        row_count += 1
        
        total_label = tk.Label(
            cart_frame, 
            text=f"Total: RM{total_price:.2f}", 
            font=('Helvetica', 14, 'bold'), 
            bg="#2d3748", 
            fg="#10b981"
        )
        total_label.grid(row=row_count, column=0, sticky="ew", padx=10, pady=5)

def remove_from_cart(item_name):
    """
    Removes a single instance of an item from the cart.
    """
    for item in cart_items:
        if item['name'] == item_name:
            cart_items.remove(item)
            print(f"Removed one {item_name} from cart.")
            break # Exit the loop after removing one instance
    update_cart_display()


def addtoCart(item):
    """
    Adds a selected item to the shopping cart.
    """
    cart_items.append(item)
    print(f"Added {item['name']} to cart. Cart now has {len(cart_items)} items.")
    # Update the display after adding an item
    update_cart_display()


def create_menu_items(parent_frame, food_data):
    """
    Dynamically creates and displays a card for each food item.
    """
    # Start placing cards from row 1 to leave room for the title in row 0
    row, col = 1, 0
    for item in food_data:
        # Create a new Frame to serve as the "card" for each item
        item_card = tk.Frame(parent_frame, bg=CardBG, relief=tk.GROOVE, borderwidth=2)
        item_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Make the single column inside the item card expandable
        item_card.grid_columnconfigure(0, weight=1)

        # --- Widgets inside the card ---
        # Item Name Label
        name_label = tk.Label(item_card, text=item['name'], font=('Helvetica', 14, 'bold'), bg=CardBG, fg=MainFG)
        name_label.grid(row=0, column=0, pady=(10, 5))
        
        # Item Description Label
        desc_label = tk.Label(item_card, text=item['description'], font=('Helvetica', 10), wraplength=200, bg=CardBG, fg=MainFG)
        desc_label.grid(row=1, column=0, padx=10)
        
        # Item Price Label
        price_label = tk.Label(item_card, text=f"RM{item['price']:.2f}", font=('Helvetica', 12, 'bold'), bg=CardBG, fg=MainFG)
        price_label.grid(row=2, column=0, pady=(5, 10))
        
        # Add to Cart Button
        # We use a lambda to pass the specific 'item' to the addtoCart function
        add_button = tk.Button(item_card, text="Add to Cart", font=('Helvetica', 10, 'bold'), bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", relief="flat", command=lambda i=item: addtoCart(i))
        add_button.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

        # Update the grid position for the next card
        col += 1
        if col > 2:  # 3 columns per row
            col = 0
            row += 1

# Main application setup
root = tk.Tk()
root.title("Cinema Food Kiosk")
root.geometry("800x600")
root.config(bg=MainBG)

# We use a grid to separate the menu and the cart
root.grid_columnconfigure(0, weight=3) # Menu column
root.grid_columnconfigure(1, weight=1) # Cart column
root.grid_rowconfigure(0, weight=1)

# Frame for the food menu on the left
menu_frame = tk.Frame(root, bg=MainBG)
menu_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Make the columns in the menu_frame expandable
menu_frame.grid_columnconfigure(0, weight=1)
menu_frame.grid_columnconfigure(1, weight=1)
menu_frame.grid_columnconfigure(2, weight=1)

# Frame for the shopping cart on the right
cart_frame = tk.Frame(root, bg="#2d3748", relief=tk.SOLID, borderwidth=1)
cart_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

# Make the columns in the cart_frame expandable
cart_frame.grid_columnconfigure(0, weight=1)

# Add main titles to each frame
menu_title_label = tk.Label(menu_frame, text="Select Your Food and Drinks", font=('Helvetica', 18, 'bold'), bg=MainBG, fg=MainFG)
menu_title_label.grid(row=0, column=0, columnspan=3, pady=10)

cart_title_label = tk.Label(cart_frame, text="Your Cart", font=('Helvetica', 18, 'bold'), bg="#2d3748", fg=MainFG)
cart_title_label.grid(row=0, column=0, pady=10, sticky="ew")

# Open the JSON data and create the menu
food_data = open_json_db()
if food_data:
    create_menu_items(menu_frame, food_data)
    
root.mainloop()
