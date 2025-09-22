import tkinter as tk
from tkinter import messagebox

import Fud
import mingsong
import seat

root = tk.Tk()
root.title("Main Page")
root.geometry("400x300")    
root.configure(bg="lightblue")
root.resizable(False, False)
header = tk.Label(root, text="Welcome to the Cinema Booking System", font=("Arial", 16, "bold"), bg="lightblue")
header.pack(pady=20)
def open_seat_booking():
    root.withdraw()  # Hide main window
    seat.root.deiconify()  # Show seat booking window
    seat.root.protocol("WM_DELETE_WINDOW", on_seat_window_close)  # Handle seat window close
def on_seat_window_close():
    seat.root.withdraw()  # Hide seat booking window
    root.deiconify()  # Show main window
    seat.root.protocol("WM_DELETE_WINDOW", on_seat_window_close)  # Reassign protocol
def open_food_ordering():
    root.withdraw()  # Hide main window
    Fud.root.deiconify()  # Show food ordering window
    Fud.root.protocol("WM_DELETE_WINDOW", on_food_window_close)  # Handle food window close
def on_food_window_close():
    Fud.root.withdraw()  # Hide food ordering window
    root.deiconify()  # Show main window
    Fud.root.protocol("WM_DELETE_WINDOW", on_food_window_close)  # Reassign protocol
def open_mingsong():
    root.withdraw()  # Hide main window
    mingsong.root.deiconify()  # Show mingsong window
    mingsong.root.protocol("WM_DELETE_WINDOW", on_mingsong_window_close)  # Handle mingsong window close
def on_mingsong_window_close():
    mingsong.root.withdraw()  # Hide mingsong window
    root.deiconify()  # Show main window
    mingsong.root.protocol("WM_DELETE_WINDOW", on_mingsong_window_close)  # Reassign protocol
seat_btn = tk.Button(root, text="Seat Booking", font=("Arial", 14), bg="green", fg="white", command=open_seat_booking)
seat_btn.pack(pady=10)
food_btn = tk.Button(root, text="Food Ordering", font=("Arial", 14), bg="orange", fg="white", command=open_food_ordering)
food_btn.pack(pady=10)
mingsong_btn = tk.Button(root, text="MingSong", font=("Arial", 14), bg="purple", fg="white", command=open_mingsong)
mingsong_btn.pack(pady=10)
root.mainloop()

