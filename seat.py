
import tkinter as tk
from tkinter import messagebox

#detail of seat
rows_top = ["A", "B", "C", "D"]    
rows_bottom = ["E", "F", "G"] 

seat_map = {}
selected_seats = []  
seat_btn = {} 

# Fill seat map
for row in rows_top:
    for num in range(1, 9):  # 1–8 seats
        seat_map[f"{row}{num}"] = False
for row in rows_bottom:
    for num in range(1, 11):  # 1–10 seats
        seat_map[f"{row}{num}"] = False

def choose_seat(seat, btn):
    if seat_map[seat]:  # Already booked
        messagebox.showwarning("Unavailable", f"Seat {seat} is already booked ❌")
        return
    
    if seat in selected_seats:  
        # Deselect
        selected_seats.remove(seat)
        btn.config(bg="green")  # back to available
    else:
        # Select
        selected_seats.append(seat)
        btn.config(bg="orange")  # selected

root = tk.Tk()
root.title("Cinema Seat Booking")
root.geometry("1000x650")

header_pg = tk.Label(root, text="🎬 Cinema Seat Booking System",
                 font=("Arial", 18, "bold"), fg="white", bg="grey")
header_pg.pack(pady=10)

screen = tk.Label (root, text="[----------------------------------------------------]",font="black", width=30, height=2)
screen.pack(pady=10)

seat_frame = tk.Frame(root)
seat_frame.pack(pady=20)



for r, row in enumerate(rows_top):
    tk.Label(seat_frame, text=row,font=("Arial", 12, "bold")).grid(row=r, column=0, padx=10)

    for c in range(1, 9):
        seat = f"{row}{c}"
        btn = tk.Button(seat_frame, text=str(c), width=4, height=2,
                        bg="green", fg="white", font=("Arial", 10, "bold"))
        btn.grid(row=r, column=c+1, padx=5, pady=5)  # shift +1 for centering
        btn.config(command=lambda s=seat, b=btn: choose_seat(s, b))
        seat_btn[seat] = btn


    tk.Label(seat_frame, text=row,font=("Arial", 12, "bold")).grid(row=r, column=10, padx=10)


gap_row = len(rows_top)
tk.Label(seat_frame).grid(row=gap_row, column=0, pady=20)




for r, row in enumerate(rows_bottom, start=gap_row + 1):
    tk.Label(seat_frame, text=row,font=("Arial", 12, "bold")).grid(row=r, column=0, padx=10)

    for c in range(1, 11):
        seat = f"{row}{c}"
        btn = tk.Button(seat_frame, text=str(c), width=4, height=2,
                        bg="green", fg="white", font=("Arial", 10, "bold"))
        btn.grid(row=r, column=c, padx=5, pady=5)
        btn.config(command=lambda s=seat, b=btn: choose_seat(s, b))
        seat_btn[seat] = btn




    tk.Label(seat_frame, text=row,font=("Arial", 12, "bold")).grid(row=r, column=11, padx=10)


root.mainloop()

