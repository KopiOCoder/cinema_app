import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import customtkinter as ctk
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import json
import os
import uuid

MainBG = "#111827"
MainFG = "#ffffff"
CardBG = "#1f2937"

def open_json_db(path="FoodDrinks.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def show_food_page(parent, checkout_callback=None, json_path="FoodDrinks.json"):
    """
    Create and return a frame attached to `parent` that implements the food kiosk.
    - parent: container widget (for example root)
    - checkout_callback: optional function(cart_items_list) called on checkout
    - json_path: path to JSON data
    """
    # Internal state
    cart_items = []

    # Helper functions
    def add_to_cart(item):
        cart_items.append(item)
        update_cart_display()

    def remove_from_cart(item_name):
        for i, it in enumerate(cart_items):
            if it["name"] == item_name:
                del cart_items[i]
                break
        update_cart_display()

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
    
        
        pay_win = tk.Toplevel(food_frame)
        pay_win.title("💳 Card Payment")
        pay_win.geometry("500x500")
        pay_win.config(bg=MainBG)
        pay_win.grab_set()

        pay_win.protocol("WM_DELETE_WINDOW", lambda: None)
    
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
        cvv_entry = tk.Entry(pay_win)
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
    
            if not card.isdigit() or len(card) != 1:
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
        tk.Button(pay_win, text="Cancel Payment", command=lambda: pay_win.destroy(), bg="#6b7280", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
    
    def show_receipt(cart_items, total_price, last_four):
        
        receipt_win = tk.Toplevel(food_frame)
        receipt_win.title("🎥 Cinema Receipt")
        receipt_win.geometry("500x600")
        receipt_win.config(bg=MainBG)

        receipt_win.transient(food_frame)
    
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
    # Build UI
    food_frame = tk.Frame(parent, bg=MainBG)
    food_frame.pack(fill="both", expand=True, padx=10, pady=10)
    parent._food_frame = food_frame

    # Left: scrollable menu canvas
    menu_container = tk.Frame(food_frame, bg=MainBG)
    menu_container.grid(row=0, column=0, sticky="nsew", padx=(10,8), pady=10)
    food_frame.grid_columnconfigure(0, weight=3)
    food_frame.grid_columnconfigure(1, weight=1)
    food_frame.grid_rowconfigure(0, weight=1)

    menu_canvas = tk.Canvas(menu_container, bg=MainBG, highlightthickness=0)
    vsb = tk.Scrollbar(menu_container, orient="vertical", command=menu_canvas.yview)
    menu_canvas.configure(yscrollcommand=vsb.set)
    menu_canvas.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    menu_container.grid_rowconfigure(0, weight=1)
    menu_container.grid_columnconfigure(0, weight=1)

    inner_menu = tk.Frame(menu_canvas, bg=MainBG)
    canvas_window = menu_canvas.create_window((0,0), window=inner_menu, anchor="nw", tags="menu_frame")

    def on_inner_config(event):
        menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))
    inner_menu.bind("<Configure>", on_inner_config)

    def on_canvas_config(event):
        menu_canvas.itemconfig("menu_frame", width=event.width)
    menu_canvas.bind("<Configure>", on_canvas_config)

    # Title
    title_lbl = tk.Label(inner_menu, text="Select Your Food and Drinks",
                         font=("Helvetica", 18, "bold"), bg=MainBG, fg=MainFG)
    title_lbl.grid(row=0, column=0, columnspan=3, pady=10)

    # Right: cart area
    cart_frame = tk.Frame(food_frame, bg="#2d3748", relief=tk.SOLID, borderwidth=1)
    cart_frame.grid(row=0, column=1, sticky="nsew", padx=(8,10), pady=10)
    cart_frame.grid_columnconfigure(0, weight=1)

    cart_title = tk.Label(cart_frame, text="Your Cart", font=("Helvetica", 18, "bold"), bg="#2d3748", fg=MainFG)
    cart_title.grid(row=0, column=0, pady=10, sticky="ew")

    back_btn = tk.Button(cart_frame, text="Back", font=("Helvetica", 14, "bold"),
                        bg="#6b7280", fg="#ffffff", command=lambda:go_back())
    back_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,5))
    back_btn.grid_remove()


    # Load data and populate menu
    data = open_json_db(json_path)

    # Organize by category
    categories = {}
    for it in data:
        cat = it.get("category", "Misc")
        categories.setdefault(cat, []).append(it)

    row = 1
    for cat, items in categories.items():
        lbl = tk.Label(inner_menu, text=cat, font=("Helvetica", 16, "bold"), bg=MainBG, fg=MainFG, pady=8)
        lbl.grid(row=row, column=0, columnspan=3, sticky="ew")
        row += 1

        col = 0
        for item in items:
            card = tk.Frame(inner_menu, bg=CardBG, relief=tk.GROOVE, borderwidth=2)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            name = tk.Label(card, text=item["name"], font=("Helvetica", 14, "bold"), bg=CardBG, fg=MainFG)
            name.grid(row=0, column=0, pady=(8,4))

            desc = tk.Label(card, text=item.get("description",""), font=("Helvetica", 10), wraplength=220, bg=CardBG, fg=MainFG)
            desc.grid(row=1, column=0, padx=6)

            price = tk.Label(card, text=f"${item['price']:.2f}", font=("Helvetica", 12, "bold"), bg=CardBG, fg=MainFG)
            price.grid(row=2, column=0, pady=(6,8))

            add = tk.Button(card, text="Add to Cart", font=("Helvetica", 10, "bold"),
                            bg="#10b981", fg="white", activebackground="#059669",
                            activeforeground="white", relief="flat", command=lambda it=item: add_to_cart(it))
            add.grid(row=3, column=0, pady=(0,8), padx=8, sticky="ew")

            col += 1
            if col > 2:
                col = 0
                row += 1
        row += 1

    # Cart UI updater
    def update_cart_display():
        # clear dynamic widgets but keep title and pay button
        for w in list(cart_frame.winfo_children()):
            if w not in (cart_title, back_btn):
                w.destroy()

        item_counts = {}
        total = 0.0
        for it in cart_items:
            name = it["name"]
            item_counts.setdefault(name, {"qty":0, "price":it["price"]})
            item_counts[name]["qty"] += 1
            total += it["price"]

        r = 2
        for name, info in item_counts.items():
            qty = info["qty"]
            subtotal = qty * info["price"]

            item_fr = tk.Frame(cart_frame, bg="#2d3748")
            item_fr.grid(row=r, column=0, sticky="ew", padx=8, pady=4)
            item_fr.grid_columnconfigure(0, weight=1)

            lbl = tk.Label(item_fr, text=f"{name} x{qty} - ${subtotal:.2f}", font=("Helvetica", 12),
                           bg="#2d3748", fg=MainFG, anchor="w")
            lbl.grid(row=0, column=0, sticky="ew")

            rem = tk.Button(item_fr, text="X", font=("Helvetica", 10, "bold"),
                            bg="#dc2626", fg="white", activebackground="#991b1b",
                            activeforeground="white", relief="flat", command=lambda n=name: remove_from_cart(n))
            rem.grid(row=0, column=1, sticky="e", padx=6)

            r += 1

        if cart_items:
            sep = tk.Frame(cart_frame, height=2, bg=MainFG)
            sep.grid(row=r, column=0, sticky="ew", padx=8, pady=6)
            r += 1

            tot_lbl = tk.Label(cart_frame, text=f"Total: ${total:.2f}", font=("Helvetica", 14, "bold"),
                               bg="#2d3748", fg="#10b981")
            tot_lbl.grid(row=r, column=0, sticky="ew", padx=8, pady=4)

            chk_btn = tk.Button(cart_frame, text="Confirm and Checkout", font=("Helvetica", 14, "bold"),
                                bg="#10b981", fg="#ffffff", command=lambda:checkout())
            chk_btn.grid(row=r+1, column=0, sticky="ew", padx=8, pady=6)

    def go_back():
        food_frame.pack_forget()
        existing_main = getattr(parent, "_main_frame", None)
        if existing_main is not None:
            existing_main.pack(fill="both", expand=True)
        else:
            food_frame.destroy()

    # Expose update to inner scope and run initial update
    update_cart_display()

    # Return the root frame so caller can manage packing/unpacking
    return food_frame