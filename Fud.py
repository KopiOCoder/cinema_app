import tkinter as tk
from tkinter import font
import json
from tkinter import messagebox, ttk
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from tkinter import filedialog
import uuid


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
    # Clear all existing widgets in the cart frame, except for the title and permanent buttons
    for widget in cart_frame.winfo_children():
        if widget is not cart_title_label and widget is not pay_button:
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
    row_count = 2  # Start from row 2 to accommodate the title and skip button
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
            text=f"{item_name} x{quantity} - ${subtotal:.2f}",
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
            text=f"Total: ${total_price:.2f}", 
            font=('Helvetica', 14, 'bold'), 
            bg="#2d3748", 
            fg="#10b981"
        )
        total_label.grid(row=row_count, column=0, sticky="ew", padx=10, pady=5)

        checkout_button = tk.Button(
            cart_frame, 
            text="Checkout", 
            font=('Helvetica', 14, 'bold'), 
            bg="#10b981", 
            fg="#ffffff",
            command=checkout
        )
        checkout_button.grid(row=row_count+1, column=0, sticky="ew", padx=10, pady=5)

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
    Dynamically creates and displays a card for each food item, grouped by category.
    """
    # Group items by category
    categories = {}
    for item in food_data:
        category = item.get('category', 'Misc') # Default to 'Misc' if no category is found
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    row = 1 # Start from row 1 to leave space for the main title
    for category_name, items in categories.items():
        # Add a label for the category
        category_label = tk.Label(
            parent_frame,
            text=category_name,
            font=('Helvetica', 16, 'bold'),
            bg=MainBG,
            fg=MainFG,
            pady=10
        )
        category_label.grid(row=row, column=0, columnspan=3, sticky="ew")
        row += 1

        # Place the items for the current category
        col = 0
        for item in items:
            # Create a new Frame for each item card
            item_card = tk.Frame(parent_frame, bg=CardBG, relief=tk.GROOVE, borderwidth=2)
            item_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            item_card.grid_columnconfigure(0, weight=1)

            # --- Widgets inside the card ---
            name_label = tk.Label(item_card, text=item['name'], font=('Helvetica', 14, 'bold'), bg=CardBG, fg=MainFG)
            name_label.grid(row=0, column=0, pady=(10, 5))
            
            desc_label = tk.Label(item_card, text=item['description'], font=('Helvetica', 10), wraplength=200, bg=CardBG, fg=MainFG)
            desc_label.grid(row=1, column=0, padx=10)
            
            price_label = tk.Label(item_card, text=f"${item['price']:.2f}", font=('Helvetica', 12, 'bold'), bg=CardBG, fg=MainFG)
            price_label.grid(row=2, column=0, pady=(5, 10))
            
            add_button = tk.Button(item_card, text="Add to Cart", font=('Helvetica', 10, 'bold'), bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", relief="flat", command=lambda i=item: addtoCart(i))
            add_button.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

            # Update the grid position for the next card
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        row += 1 # Move to the next row after a full row of items, or to prepare for the next category header

def checkout():
    """
    Checkout process with card payment UI.
    Opens a payment window, validates card info,
    and clears cart after successful payment.
    """
    if not cart_items:
        print("\n--- CHECKOUT ABORTED ---")
        print("Your cart is empty. Nothing to check out.")
        print("------------------------\n")
        return

    
    pay_win = tk.Toplevel(root)
    pay_win.title("💳 Card Payment")
    pay_win.geometry("400x400")
    pay_win.config(bg=MainBG)
    pay_win.grab_set()

    tk.Label(pay_win, text="💳 Card Payment", font=("Arial", 16, "bold"), bg=MainBG, fg="white").pack(pady=10)

    
    countdown_label = tk.Label(pay_win, text="Time Remaining: 180", font=("Arial", 10, "bold"), fg="green", bg=MainBG)
    countdown_label.pack(pady=5)
    time_remaining = [180]
    timer_id = [None]

    def countdown_timer():
        if time_remaining[0] > 0:
            time_remaining[0] -= 1
            countdown_label.config(text=f"Time Remaining: {time_remaining[0]}")
            if time_remaining[0] < 30:
                countdown_label.config(fg="red")
            timer_id[0] = pay_win.after(1000, countdown_timer)
        else:
            tk.messagebox.showwarning("Timeout", "Order cancelled due to timeout.")
            pay_win.destroy()

    countdown_timer()

    
    tk.Label(pay_win, text="Card Number (16 digits):", bg=MainBG, fg="white").pack(pady=2)
    card_entry = tk.Entry(pay_win)
    card_entry.pack()

    tk.Label(pay_win, text="CVV (3 digits):", bg=MainBG, fg="white").pack(pady=2)
    cvv_entry = tk.Entry(pay_win, show="*")
    cvv_entry.pack()

    tk.Label(pay_win, text="Expiry Date (MM/YY):", bg=MainBG, fg="white").pack(pady=2)
    expiry_entry = tk.Entry(pay_win)
    expiry_entry.pack()

    status_label = tk.Label(pay_win, text="", fg="red", bg=MainBG)
    status_label.pack(pady=5)

    progress_bar = ttk.Progressbar(pay_win, orient="horizontal", mode="indeterminate")

    #Payment 
    def process_payment():
        card = card_entry.get()
        cvv = cvv_entry.get()
        expiry = expiry_entry.get()

        if not card.isdigit() or len(card) != 16:
            status_label.config(text="❌ Invalid card number.")
            return
        if not cvv.isdigit() or len(cvv) != 3:
            status_label.config(text="❌ Invalid CVV.")
            return
        if len(expiry) != 5 or expiry[2] != '/':
            status_label.config(text="❌ Invalid expiry date format.")
            return

        try:
            exp_month = int(expiry[:2])
            exp_year = int(expiry[3:]) + 2000
            now = datetime.datetime.now()
            if exp_month < 1 or exp_month > 12:
                status_label.config(text="❌ Invalid expiry month.")
                return
            if exp_year < now.year or (exp_year == now.year and exp_month < now.month):
                status_label.config(text="❌ Card expired.")
                return
        except ValueError:
            status_label.config(text="❌ Invalid expiry date.")
            return

        #cancel timer
        if timer_id[0]:
            pay_win.after_cancel(timer_id[0])

        #Simulate phone authorization
        def show_approval():
            auth_win = tk.Toplevel(pay_win)
            auth_win.title("Authorization")
            auth_win.geometry("300x120")
            auth_win.transient(pay_win)
            auth_win.grab_set()

            tk.Label(auth_win, text="Authorization request sent to phone.", font=("Arial", 10)).pack(pady=10)
            tk.Button(auth_win, text="I've Authorized/Rejected",
                      command=lambda: (auth_win.destroy(), authorize_payment())
                      , bg="green", fg="white").pack(pady=5)

        def authorize_payment():
            status_label.config(text="Processing payment...")
            progress_bar.pack(pady=10)
            progress_bar.start(3)
            pay_win.after(3000, payment_complete)

        def payment_complete():
                progress_bar.stop()
                progress_bar.pack_forget()

                #Prepare receipt data BEFORE clearing the cart
                cart_items_copy = cart_items.copy()
                total_price = sum(item['price'] for item in cart_items_copy)
                last_four = card[-4:]

                # Clear cart and update UI
                cart_items.clear()
                update_cart_display()

                # Show receipt (uses the copied list and computed total)
                show_receipt(cart_items_copy, total_price, last_four)

                messagebox.showinfo("Payment Status", "Payment successful! Enjoy your order 🎉")
                pay_win.destroy()

        show_approval()

    tk.Button(pay_win, text="Pay", command=process_payment, bg="#10b981", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

def show_receipt(cart_items, total_price, last_four):
    
    receipt_win = tk.Toplevel(root)
    receipt_win.title("🎥 Cinema Receipt")
    receipt_win.geometry("500x600")
    receipt_win.config(bg=MainBG)

    title = tk.Label(receipt_win, text="🎥 Cinema Food Receipt", 
                     font=("Arial", 16, "bold"), bg=MainBG, fg="white")
    title.pack(pady=10)

    # Build receipt text
    current = datetime.datetime.now()
    receipt_time = current.strftime("%I:%M %p")
    receipt_date = current.strftime("%d %B %Y")
    transaction_id = str(uuid.uuid4())[:8]  # shorten UUID

    receipt_text = (
        f"Transaction ID: {transaction_id}\n"
        f"Date: {receipt_date}\n"
        f"Time: {receipt_time}\n"
        f"------------------------------\n"
    )

    for item in cart_items:
        receipt_text += f"{item['name']} - ${item['price']:.2f}\n"

    receipt_text += (
        f"------------------------------\n"
        f"Total Paid: ${total_price:.2f}\n"
        f"Paid by Card: ************{last_four}\n"
        f"==============================\n"
        f"Thank you for your visit! 🎟️\n\n"
        f"Terms & Conditions:\n"
        f"- Food are non-refundable and non-exchangeable.\n"
        f"- Please arrive on time.\n"
        f"- Lost or damaged items cannot be replaced.\n"
        f"- Management reserves the right to refuse service."
    )

    receipt_label = tk.Label(receipt_win, text=receipt_text, 
                             justify="left", font=("Courier", 11), 
                             bg=MainBG, fg="white", anchor="w")
    receipt_label.pack(padx=20, pady=10, fill="both", expand=True)

    def save_as_pdf():
        try:
            now = datetime.datetime.now()
            filename = now.strftime("CinemaReceipt_%Y-%m-%d_%H%M%S")

            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Receipt as PDF",
                initialfile=filename
            )
            if not file_path:
                return

            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'],
                                         fontSize=20, alignment=TA_CENTER,
                                         spaceAfter=12)
            story.append(Paragraph("Cinema Ticket Receipt", title_style))
            story.append(Spacer(1, 12))

            for line in receipt_text.split('\n'):
                story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 6))

            doc.build(story)
            messagebox.showinfo("Success", f"Receipt saved to:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {e}")

    tk.Button(receipt_win, text="Save as PDF", command=save_as_pdf, 
              bg="#10b981", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(receipt_win, text="Close", command=receipt_win.destroy, 
              bg="#6b7280", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

# Main application setup
root = tk.Tk()
root.title("Cinema Food Kiosk")
root.geometry("800x600+0+0")
root.config(bg=MainBG)

# --- Layout Frames ---
# The main grid is now simpler
root.grid_columnconfigure(0, weight=3, uniform="group1") # Menu column
root.grid_columnconfigure(1, weight=1, uniform="group1") # Cart column
root.grid_rowconfigure(0, weight=1)

# Create a master frame for the menu area to contain the canvas and scrollbar
menu_frame = tk.Frame(root, bg=MainBG)
menu_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# --- Scrollable Menu ---
# Place the canvas and scrollbar inside the new menu_frame
menu_frame.grid_columnconfigure(0, weight=1)  # Canvas column
menu_frame.grid_columnconfigure(1, weight=0, minsize=20)  # Scrollbar column
menu_frame.grid_rowconfigure(0, weight=1)

menu_canvas = tk.Canvas(menu_frame, bg=MainBG, highlightthickness=0)
menu_canvas.grid(row=0, column=0, sticky="nsew")

menu_scrollbar = tk.Scrollbar(menu_frame, orient="vertical", command=menu_canvas.yview)
menu_scrollbar.grid(row=0, column=1, sticky="ns")
menu_canvas.configure(yscrollcommand=menu_scrollbar.set)

# Frame inside the canvas
scrollable_menu_frame = tk.Frame(menu_canvas, bg=MainBG)
# Give the created window a tag so we can resize it later
menu_canvas_window = menu_canvas.create_window(
    (0, 0),
    window=scrollable_menu_frame,
    anchor="nw",
    tags="menu_frame"
)

# Expand columns inside scrollable frame
scrollable_menu_frame.grid_columnconfigure(0, weight=1)
scrollable_menu_frame.grid_columnconfigure(1, weight=1)
scrollable_menu_frame.grid_columnconfigure(2, weight=1)

# Update scrollregion when frame grows
def on_frame_configure(event):
    menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))

scrollable_menu_frame.bind("<Configure>", on_frame_configure)

# Keep inner frame width synced with canvas width
def on_canvas_configure(event):
    menu_canvas.itemconfig("menu_frame", width=event.width)

menu_canvas.bind("<Configure>", on_canvas_configure)

# Cross-platform mousewheel scrolling
def on_mousewheel(event):
    if event.num == 4:  # Linux scroll up
        menu_canvas.yview_scroll(-1, "units")
    elif event.num == 5:  # Linux scroll down
        menu_canvas.yview_scroll(1, "units")
    else:  # Windows/Mac
        menu_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

menu_canvas.bind_all("<MouseWheel>", on_mousewheel)   # Windows/Mac
menu_canvas.bind_all("<Button-4>", on_mousewheel)    # Linux scroll up
menu_canvas.bind_all("<Button-5>", on_mousewheel)    # Linux scroll down


# --- Cart Frame ---
cart_frame = tk.Frame(root, bg="#2d3748", relief=tk.SOLID, borderwidth=1)
cart_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

cart_frame.grid_columnconfigure(0, weight=1)

# Add main titles to each frame
menu_title_label = tk.Label(scrollable_menu_frame, text="Select Your Food and Drinks", font=('Helvetica', 18, 'bold'), bg=MainBG, fg=MainFG)
menu_title_label.grid(row=0, column=0, columnspan=3, pady=10)

cart_title_label = tk.Label(cart_frame, text="Your Cart", font=('Helvetica', 18, 'bold'), bg="#2d3748", fg=MainFG)
cart_title_label.grid(row=0, column=0, pady=10, sticky="ew")

# The permanent " Pay" button
pay_button = tk.Button(
    cart_frame,
    text="Pay",
    font=('Helvetica', 14, 'bold'),
    bg="#6b7280",
    fg="#ffffff",
    command=checkout
)
pay_button.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))

# Open the JSON data and create the menu
food_data = open_json_db()
if food_data:
    create_menu_items(scrollable_menu_frame, food_data)

# Call update_cart_display to show the initial state of the cart
update_cart_display()
    
root.mainloop()
