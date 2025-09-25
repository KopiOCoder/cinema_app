import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import os

rows_top = ["A", "B", "C", "D"]
rows_bottom = ["E", "F", "G"]

def init_db(db_path):
    cnct = sqlite3.connect(db_path)
    cur = cnct.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            row TEXT NOT NULL,
            number INTEGER NOT NULL,
            booked INTEGER DEFAULT 0
        )
    """)
    # Optionally, populate seats if not already present
    for row in rows_top + rows_bottom:
        for num in range(1, 11):
            cur.execute("SELECT * FROM seats WHERE row=? AND number=?", (row, num))
            if not cur.fetchone():
                cur.execute("INSERT INTO seats (row, number, booked) VALUES (?, ?, 0)", (row, num))
    cnct.commit()
    cnct.close()

def get_seat_status(db_path):
    cnct = sqlite3.connect(db_path)
    cur = cnct.cursor()
    cur.execute("SELECT row, number, booked FROM seats")
    status = {}
    for row, num, booked in cur.fetchall():
        status[f"{row}{num}"] = booked
    cnct.close()
    return status

def book_seat(db_path, seat_name):
    row = seat_name[0]
    num = int(seat_name[1:])
    cnct = sqlite3.connect(db_path)
    cur = cnct.cursor()
    cur.execute("UPDATE seats SET booked=1 WHERE row=? AND number=?", (row, num))
    cnct.commit()
    cnct.close()

def show_seat_page(root, movie_title):
    root._main_frame.pack_forget()
    db_path = f"{movie_title.replace(' ', '_')}.db"
    init_db(db_path)
    seat_status = get_seat_status(db_path)
    selected_seats = []

    seat_frame = ctk.CTkFrame(root)
    seat_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    seat_label = ctk.CTkLabel(seat_frame, text=f"Seat Selection for {movie_title}", font=("Arial", 20, "bold"))
    seat_label.pack(pady=20)

    grid_frame = ctk.CTkFrame(seat_frame)
    grid_frame.pack(pady=10)

    seat_btns = {}

    def choose_seat(seat_name):
        if seat_status[seat_name]:
            messagebox.showwarning("Unavailable", f"Seat {seat_name} is already booked.")
            return
        if seat_name in selected_seats:
            selected_seats.remove(seat_name)
            seat_btns[seat_name].configure(fg_color="#222")
        else:
            selected_seats.append(seat_name)
            seat_btns[seat_name].configure(fg_color="#0af")

    # Create seat buttons
    for r, row in enumerate(rows_top + rows_bottom):
        grid_col = 0
        for num in range(1, 11):
            if num in (3, 9):          # put a visual gap before seat 3 and before seat 9
                gap = ctk.CTkLabel(grid_frame, text="   ", width=20)
                gap.grid(row=r, column=grid_col, padx=4)
                grid_col += 1

            seat_name = f"{row}{num}"
            btn = ctk.CTkButton(
                grid_frame,
                text=seat_name,
                width=40,
                height=30,
                fg_color="#888" if seat_status.get(seat_name, 0) else "#222",
                command=lambda sn=seat_name: choose_seat(sn)
            )
            btn.grid(row=r, column=grid_col, padx=4, pady=4)
            seat_btns[seat_name] = btn
            grid_col += 1

    def proceed_payment():
        if not selected_seats:
            messagebox.showwarning("No Selection", "Please select at least one seat")
            return
        import subprocess
        seats_str = ",".join(selected_seats)
        seat_count = len(selected_seats)
        subprocess.call(["python", "PaymentandFare.py", movie_title, str(seat_count), seats_str])
        messagebox.showinfo("Payment", "Payment successful! Seats booked.")
        seat_frame.pack_forget()
        root._main_frame.pack(
            side="left", fill="both", expand=True, padx=20, pady=20
        )
        # Optionally, call a callback to go back to main page

    pay_btn = ctk.CTkButton(seat_frame, text="Proceed to Payment", command=proceed_payment)
    pay_btn.pack(pady=20)

    def go_back():
        seat_frame.pack_forget()
        root._main_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    back_btn = ctk.CTkButton(seat_frame, text="Back", command=go_back)
    back_btn.pack(pady=4)

    return seat_frame