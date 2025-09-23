import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import time
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import uuid



#Calculates the total fare based on the number of adults and children
def calculate_fare(num_adults, num_children):
    ADULT_PRICE = 15.00
    CHILD_PRICE = 10.00
    return (num_adults * ADULT_PRICE) + (num_children * CHILD_PRICE)

def return_to_ticket_selection(self):
        self.controller.show_frame("TicketSelectionFrame")


#tkinter setup (Manages frames, and variables)

class CinemaKiosk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema Kiosk")
        self.geometry("1000x650") 
        self.resizable(False, False)

        
        #shared variables
        self.num_adults = 0
        self.num_children = 0
        self.total_price = 0.0
        self.last_four_card_digits = None
        self.transaction_id = None
        self.frames = {}


        #frames arrangement
        self.frames = {}
        for F in (SeatSelectionFrame, SummaryFrame, PaymentFrame, ReceiptFrame):
            frame = F(self, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #start with ticket selection frame
        self.show_frame("SeatSelectionFrame")

    #Show a frame for the given page name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

"""
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

    def tkraise(self, *args, **kwargs):
        # Clears the entry fields and status label when this frame is shown
        self.adult_entry.delete(0, tk.END)
        self.child_entry.delete(0, tk.END)
        self.status_label.config(text="")
        super().tkraise(*args, **kwargs)


    #validation
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
"""

#detail of seat
rows_top = ["A", "B", "C", "D"]
rows_bottom = ["E", "F", "G"]

class SeatSelectionFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Data for seat booking
        self.seat_map = {}
        self.selected_seats = []
        self.seat_buttons = {}

        # Fill seat map initially
        for row in rows_top:
            for num in range(1, 9):
                self.seat_map[f"{row}{num}"] = False
        for row in rows_bottom:
            for num in range(1, 11):
                self.seat_map[f"{row}{num}"] = False

        # UI elements
        title = tk.Label(self, text="🎬 Select Your Seats", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        screen_label = tk.Label(self, text="SCREEN", bg="black", fg="white", font=("Arial", 12))
        screen_label.pack(fill="x", padx=20, pady=10)

        seat_frame = tk.Frame(self)
        seat_frame.pack()

        # Top rows (A-D)
        for r, row in enumerate(rows_top):
            tk.Label(seat_frame, text=row, font=("Arial", 12, "bold")).grid(row=r, column=0, padx=10)
            for c in range(1, 9):
                seat = f"{row}{c}"
                btn = tk.Button(seat_frame, text=str(c), width=4, height=2,
                                bg="green", fg="white", font=("Arial", 10, "bold"),
                                command=lambda s=seat: self.toggle_seat(s))
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.seat_buttons[seat] = btn
            tk.Label(seat_frame, text=row, font=("Arial", 12, "bold")).grid(row=r, column=10, padx=10)

        # Gap row
        gap_row = len(rows_top)
        tk.Label(seat_frame).grid(row=gap_row, column=0, pady=10)

        # Bottom rows (E-G)
        for r, row in enumerate(rows_bottom, start=gap_row + 1):
            tk.Label(seat_frame, text=row, font=("Arial", 12, "bold")).grid(row=r, column=0, padx=10)
            for c in range(1, 11):
                seat = f"{row}{c}"
                btn = tk.Button(seat_frame, text=str(c), width=4, height=2,
                                bg="green", fg="white", font=("Arial", 10, "bold"),
                                command=lambda s=seat: self.toggle_seat(s))
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.seat_buttons[seat] = btn
            tk.Label(seat_frame, text=row, font=("Arial", 12, "bold")).grid(row=r, column=11, padx=10)

        self.status_label = tk.Label(self, text="", fg="red")
        self.status_label.pack(pady=5)
        self.selected_label = tk.Label(self, text="Selected Seats: 0", font=("Arial", 10))
        self.selected_label.pack()

        tk.Button(self, text="Proceed to Summary", command=self.proceed_to_summary).pack(pady=10)

    def toggle_seat(self, seat_id):
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
            self.seat_buttons[seat_id].config(bg="green", relief=tk.RAISED)
        elif self.seat_map[seat_id] == False:
            self.selected_seats.append(seat_id)
            self.seat_buttons[seat_id].config(bg="blue", relief=tk.SUNKEN)
        else:
            messagebox.showinfo("Seat Booked", "Sorry, this seat is already booked.")
        self.update_labels()

    def update_labels(self):
        self.selected_label.config(text=f"Selected Seats: {', '.join(self.selected_seats)}")
    
    def proceed_to_summary(self):
        num_seats = len(self.selected_seats)
        if num_seats == 0:
            self.status_label.config(text="Please select at least one seat.")
            return

        # Simple logic: all selected tickets are adult tickets
        self.controller.num_adults = num_seats
        self.controller.num_children = 0
        self.controller.total_price = calculate_fare(num_seats, 0)
        self.controller.show_frame("SummaryFrame")

    def tkraise(self, *args, **kwargs):
        # Reset frame when shown
        self.selected_seats.clear()
        self.update_labels()
        for seat, btn in self.seat_buttons.items():
            if not self.seat_map[seat]:
                btn.config(bg="green", relief=tk.RAISED)
        super().tkraise(*args, **kwargs)

#Frame 2: Order Summary
class SummaryFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.selected_seats = []
        self.controller = controller

        title = tk.Label(self, text="🎬 Order Summary", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        self.summary_label = tk.Label(self, text="", font=("Arial", 12))
        self.summary_label.pack(pady=5)

        self.seats_label = tk.Label(self, text="", font=("Arial", 12))
        self.seats_label.pack(pady=5)

        tk.Button(self, text="Proceed to Payment", command=lambda: controller.show_frame("PaymentFrame")).pack(pady=10)
        tk.Button(self, text="Cancel Order", command=self.cancel_order).pack(pady=5)

    def tkraise(self, *args, **kwargs):
        #Update summary 
        adults = self.controller.num_adults
        children = self.controller.num_children
        total = self.controller.total_price
        selected_seats_str = ", ".join(self.controller.selected_seats)

        summary_text = f"Adult Tickets: {adults} x $15.00\nChild Tickets: {children} x $10.00\n\nTotal: ${total:.2f}"
        self.summary_label.config(text=summary_text)
        self.seats_label.config(text=f"Seats: {selected_seats_str}")
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

        #countdown timer 
        self.countdown_label = tk.Label(self, text="Time Remaining: 60", font=("Arial", 10, "bold"), fg="blue")
        self.countdown_label.pack(pady=5)
        self.time_remaining = 60
        self.timer_id = None

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

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")

    def tkraise(self, *args, **kwargs):
        #starts the countdown and timer when the frame is shown
        self.start_countdown()

        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.status_label.config(text="")
        self.card_entry.delete(0, tk.END)
        self.cvv_entry.delete(0, tk.END)
        self.expiry_entry.delete(0, tk.END)
        
        super().tkraise(*args, **kwargs)

    def start_countdown(self):
        #reset/start the countdown timer
        self.time_remaining = 180
        self.countdown_label.config(text=f"Time Remaining: {self.time_remaining}", fg="green")
        if self.timer_id:
            self.after_cancel(self.timer_id) 
        self.countdown_timer()
    
    def countdown_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.countdown_label.config(text=f"Time Remaining: {self.time_remaining}")

            #change color for a sense of urgency :D
            if self.time_remaining < 30:
                self.countdown_label.config(fg="red")

            #let it repeat
            self.timer_id = self.after(1000, self.countdown_timer) 
        else:
            self.cancel_order_timeout()

    def cancel_order_timeout(self):
        messagebox.showwarning("Order Timeout", "Order cancelled due to timeout.")
        self.controller.show_frame("TicketSelectionFrame")

    def process_payment(self):
        card = self.card_entry.get()
        cvv = self.cvv_entry.get()
        expiry = self.expiry_entry.get()

        #TESTING....REMEMBER ADJUST BACK TO 16
        if not card.isdigit() or len(card) != 16:
            self.status_label.config(text="❌ Invalid card number.")
            return
        if not cvv.isdigit() or len(cvv) != 3:
            self.status_label.config(text="❌ Invalid CVV.")
            return
        if len(expiry) != 5 or expiry[2] != '/':
            self.status_label.config(text="❌ Invalid expiry date format.")
            return
        
        try:
            exp_month = int(expiry[:2])
            exp_year = int(expiry[3:]) + 2000 

            if exp_month < 1 or exp_month > 12:
                self.status_label.config(text="❌ Invalid expiry month.")
                return

            
            now = datetime.datetime.now()
            current_year = now.year
            current_month = now.month

            #expiry check
            if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
                self.status_label.config(text="❌ Card expired.")
                return
            
        except ValueError:
            self.status_label.config(text="❌ Invalid expiry date.")
            return
            
        if self.timer_id:
            self.after_cancel(self.timer_id)

        #Store the last four digits of the card number
        self.controller.last_four_card_digits = card[-4:]

        #pop up the approval window
        self.show_approval_window()

    def show_approval_window(self):
        
        self.approval_window = tk.Toplevel(self.controller)
        self.approval_window.title("Authorization")
        self.approval_window.geometry("300x120")
        self.approval_window.transient(self.controller)
        self.approval_window.grab_set()

        tk.Label(self.approval_window, text="An authorization request has been sent to your phone.", font=("Arial", 10)).pack(pady=10)

     
        btn_frame = tk.Frame(self.approval_window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="I've Authorized/Rejected Transaction", command=self.authorize_payment, bg="green", fg="white").pack(side=tk.LEFT, padx=5)

    def authorize_payment(self):
        self.approval_window.destroy()
        self.status_label.config(text="Processing payment...")
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(3)
        self.after(3000, self.process_payment_completed)

        #Simulate payment processing
        self.status_label.config(text="Processing payment...")
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(3)
        
        self.after(1000, self.process_payment_completed)

    def process_payment_completed(self):
        self.progress_bar.stop()

        self.card_entry.delete(0, tk.END)
        self.cvv_entry.delete(0, tk.END)
        self.expiry_entry.delete(0, tk.END)

        self.controller.transaction_id = str(uuid.uuid4())
        
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

        tk.Button(self, text="Save as PDF", command=self.save_as_pdf).pack(pady=5)
        tk.Button(self, text="Close", command=self.return_to_ticket_selection).pack(pady=5)

    def tkraise(self, *args, **kwargs):
        #Update receipt details 
        current = datetime.datetime.now()
        receipt_time = current.strftime("%I:%M %p")
        receipt_date = current.strftime("%d %B %Y")
        
        adults = self.controller.num_adults
        children = self.controller.num_children
        total = self.controller.total_price
        last_four = self.controller.last_four_card_digits
        transaction_id = self.controller.transaction_id

        receipt_text = (
            f"Transaction ID: {transaction_id}\n"
            f"Date: {receipt_date}\n"
            f"Time: {receipt_time}\n"
            f"------------------------------\n"
            f"Adult Tickets: {adults} x $15.00\n"
            f"Child Tickets: {children} x $10.00\n"
            f"------------------------------\n"
            f"Total Paid: ${total:.2f}\n"
            f"Paid by Card: ************{last_four}\n"
            f"==============================\n"
            f"Thank you for your visit! 🎟️"
        )
        self.receipt_label.config(text=receipt_text)
        super().tkraise(*args, **kwargs)

    def save_as_pdf(self):
        try:
            #autofull filename with the time
            now = datetime.datetime.now()
            filename = now.strftime("CinemaReceipt_%Y-%m-%d_%H%M%S")

            #open a file dialog with the autofilled name
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Receipt as PDF",
                initialfile=filename
            )

            if not file_path: 
                return

            #create the PDF document
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            #add title to the PDF
            title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'],
                                         fontSize=20, alignment=TA_CENTER,
                                         spaceAfter=12)
            story.append(Paragraph("Cinema Ticket Receipt", title_style))
            story.append(Spacer(1, 12))

            #get the receipt text from the label and add it to the PDF
            receipt_text = self.receipt_label.cget("text")
            for line in receipt_text.split('\n'):
                #each line as new paragraph
                story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 6))

            
            doc.build(story)
            messagebox.showinfo("Success", f"Receipt saved successfully to:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {e}")

    def return_to_ticket_selection(self):
        self.controller.show_frame("TicketSelectionFrame")


#Main loop
if __name__ == "__main__":
    app = CinemaKiosk()
    app.mainloop()