import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import time
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER




def calculate_fare(num_adults, num_children):
    #Calculates the total fare based on the number of adults and children
    ADULT_PRICE = 15.00
    CHILD_PRICE = 10.00
    return (num_adults * ADULT_PRICE) + (num_children * CHILD_PRICE)

def return_to_ticket_selection(self):
        self.controller.show_frame("TicketSelectionFrame")


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

    def tkraise(self, *args, **kwargs):
        # Clears the entry fields and status label when this frame is shown
        self.adult_entry.delete(0, tk.END)
        self.child_entry.delete(0, tk.END)
        self.status_label.config(text="")
        super().tkraise(*args, **kwargs)

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
        #Update summary 
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
        #resets the timer and starts the countdown
        self.time_remaining = 10
        self.countdown_label.config(text=f"Time Remaining: {self.time_remaining}", fg="green")
        if self.timer_id:
            self.after_cancel(self.timer_id) 
        self.countdown_timer()
    
    def countdown_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.countdown_label.config(text=f"Time Remaining: {self.time_remaining}")

            #change color for a sense of urgency :D
            if self.time_remaining < 5:
                self.countdown_label.config(fg="red")
            
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
        if not card.isdigit() or len(card) != 1:
            self.status_label.config(text="❌ Invalid card number.")
            return
        if not cvv.isdigit() or len(cvv) != 3:
            self.status_label.config(text="❌ Invalid CVV.")
            return
        if len(expiry) != 5 or expiry[2] != '/':
            self.status_label.config(text="❌ Invalid expiry date format.")
            return
        
        if self.timer_id:
            self.after_cancel(self.timer_id)

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

    def save_as_pdf(self):
        try:
            #time
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