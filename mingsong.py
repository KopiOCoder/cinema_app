import tkinter as tk
from tkinter import messagebox
import time
import datetime



def calculate_fare(num_adults, num_children):
    #Calculates the total fare based on the number of adults and children
    ADULT_PRICE = 15.00
    CHILD_PRICE = 10.00
    return (num_adults * ADULT_PRICE) + (num_children * CHILD_PRICE)

#tkinter setup

class CinemaKiosk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema Kiosk")
        self.geometry("400x400")
        self.resizable(False, False)

        
        self.num_adults = 0
        self.num_children = 0
        self.total_price = 0.0

        #frames arrangement
        self.frames = {}
        for F in (TicketSelectionFrame, SummaryFrame, PaymentFrame, ReceiptFrame):
            frame = F(self, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TicketSelectionFrame")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

#Frame 1: Ticket Selection
class TicketSelectionFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="🎬 Buy Your Tickets", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        tk.Label(self, text="Adult Tickets:").pack(pady=5)
        self.adult_entry = tk.Entry(self)
        self.adult_entry.pack()

        tk.Label(self, text="Child Tickets:").pack(pady=5)
        self.child_entry = tk.Entry(self)
        self.child_entry.pack()

        tk.Button(self, text="Calculate Fare", command=self.calculate).pack(pady=20)
        self.status_label = tk.Label(self, text="", fg="red")
        self.status_label.pack()

    def calculate(self):
        try:
            adults = int(self.adult_entry.get())
            children = int(self.child_entry.get())

            if adults < 0 or children < 0:
                self.status_label.config(text="Number of tickets cannot be negative.")
                return
            
            if adults == 0 and children == 0:
                self.status_label.config(text="Please select at least one ticket.")
                return

            self.controller.num_adults = adults
            self.controller.num_children = children
            self.controller.total_price = calculate_fare(adults, children)
            self.controller.show_frame("SummaryFrame")

        except ValueError:
            self.status_label.config(text="Invalid input. Please enter a number.")

#Frame 2: Order Summary
class SummaryFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="🎬 Order Summary", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        self.summary_label = tk.Label(self, text="", font=("Arial", 12))
        self.summary_label.pack(pady=5)

        tk.Button(self, text="Proceed to Payment", command=lambda: controller.show_frame("PaymentFrame")).pack(pady=10)
        tk.Button(self, text="Cancel Order", command=self.cancel_order).pack(pady=5)

    def tkraise(self, *args, **kwargs):
        # Update summary 
        adults = self.controller.num_adults
        children = self.controller.num_children
        total = self.controller.total_price
        summary_text = f"Adult Tickets: {adults} x $15.00\nChild Tickets: {children} x $10.00\n\nTotal: ${total:.2f}"
        self.summary_label.config(text=summary_text)
        super().tkraise(*args, **kwargs)

    def cancel_order(self):
        messagebox.showinfo("Order Cancelled", "Order cancelled. Thank you for your visit!")
        self.controller.show_frame("TicketSelectionFrame")

#Frame 3: Payment
class PaymentFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="💳 Card Payment", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        tk.Label(self, text="Card Number (16 digits):").pack()
        self.card_entry = tk.Entry(self)
        self.card_entry.pack()

        tk.Label(self, text="CVV (3 digits):").pack()
        self.cvv_entry = tk.Entry(self)
        self.cvv_entry.pack()

        tk.Label(self, text="Expiry Date (MM/YY):").pack()
        self.expiry_entry = tk.Entry(self)
        self.expiry_entry.pack()

        tk.Button(self, text="Pay", command=self.process_payment).pack(pady=20)
        self.status_label = tk.Label(self, text="", fg="red")
        self.status_label.pack()

    def process_payment(self):
        card = self.card_entry.get()
        cvv = self.cvv_entry.get()
        expiry = self.expiry_entry.get()

        if not card.isdigit() or len(card) != 16:
            self.status_label.config(text="❌ Invalid card number.")
            return
        if not cvv.isdigit() or len(cvv) != 3:
            self.status_label.config(text="❌ Invalid CVV.")
            return
        if len(expiry) != 5 or expiry[2] != '/':
            self.status_label.config(text="❌ Invalid expiry date format.")
            return
        
        #Simulate payment processing
        self.status_label.config(text="Processing payment...")
        self.update_idletasks()
        time.sleep(2)
        
        messagebox.showinfo("Payment Status", "Payment successful! 🎉")
        self.controller.show_frame("ReceiptFrame")

#Frame 4: Receipt
class ReceiptFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="🎥 Cinema Ticket Receipt", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        self.receipt_label = tk.Label(self, text="", justify=tk.LEFT, font=("Courier", 12))
        self.receipt_label.pack(pady=5)

        tk.Button(self, text="Close", command=self.controller.destroy).pack(pady=20)

    def tkraise(self, *args, **kwargs):
        #Update receipt details 
        current = datetime.datetime.now()
        receipt_time = current.strftime("%I:%M %p")
        receipt_date = current.strftime("%d %B %Y")
        
        adults = self.controller.num_adults
        children = self.controller.num_children
        total = self.controller.total_price

        receipt_text = (
            f"Date: {receipt_date}\n"
            f"Time: {receipt_time}\n"
            f"------------------------------\n"
            f"Adult Tickets: {adults} x $15.00\n"
            f"Child Tickets: {children} x $10.00\n"
            f"------------------------------\n"
            f"Total Paid: ${total:.2f}\n"
            f"==============================\n"
            f"Thank you for your visit! 🎟️"
        )
        self.receipt_label.config(text=receipt_text)
        super().tkraise(*args, **kwargs)

#Main loop
if __name__ == "__main__":
    app = CinemaKiosk()
    app.mainloop()