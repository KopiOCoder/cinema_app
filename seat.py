
import tkinter as tk
from tkinter import messagebox

#detail of seat
rows_top = ["A", "B", "C", "D"]    
rows_bottom = ["E", "F", "G"] 

seat_map = {}
selected_seats = []  
seat_btn = {} 
#function of choosing seat
def choose_seat(seat, btn):
    if seat_map[seat]:  # Already booked
        messagebox.showwarning("Unavailable", f"Seat {seat} is already booked ❌")
        return
    
    if seat in selected_seats:  
        # Deselect
        selected_seats.remove(seat)
        btn.config(bg="green")  #as default
    else:
        # Select
        selected_seats.append(seat)
        btn.config(bg="orange")  # selected

#function of turning page
def detail_pg():
    if not selected_seats:
        messagebox.showwarning("No Selection", "Please select at least one seat")
        return

    dt_wdw = tk.Toplevel(root)
    dt_wdw.title("Payment")
    dt_wdw.geometry("350x400")
    
    tk.Label(dt_wdw, text="Detail    :", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(dt_wdw, text=f"Selected Seats: {', '.join(selected_seats)}",
             font=("Arial", 12)).pack(pady=10)
    
    # Adult, child, and elderly count selectors
    tk.Label(dt_wdw, text="Num of Adults:", font=("Arial", 12)).pack(pady=5)
    adult_count = tk.IntVar(value=len(selected_seats))  # default all adults
    tk.Spinbox(dt_wdw, from_=0, to=len(selected_seats), textvariable=adult_count, width=5).pack()

    tk.Label(dt_wdw, text="Num of Child:", font=("Arial", 12)).pack(pady=5)
    child_count = tk.IntVar(value=0)  # default 0 children
    tk.Spinbox(dt_wdw, from_=0, to=len(selected_seats), textvariable=child_count, width=5).pack()

    tk.Label(dt_wdw, text="Num of Old folks:", font=("Arial", 12)).pack(pady=5)
    oldfolk_count = tk.IntVar(value=0)  # default 0 elderly
    tk.Spinbox(dt_wdw, from_=0, to=len(selected_seats), textvariable=oldfolk_count, width=5).pack()
    
    def confirm_payment():
        adults = adult_count.get()
        child = child_count.get()
        oldfolk = oldfolk_count.get()
        total = adults + child + oldfolk # to make sure that the default not more than the limit num
        if total != len(selected_seats):
            messagebox.showerror("Invalid Input", "The total of adults, children, and elderly must equal selected seats.")
            return
        for seat in selected_seats:
            seat_map[seat] = True
            seat_btn[seat].config(text="❌", bg="gray", width=4, height=2)
        messagebox.showinfo(
            "Success",
            f"Seats {', '.join(selected_seats)} booked successfully ✅\n"
            f"Adults: {adults}, Children: {child}, Olf folk: {oldfolk}"
        )
        selected_seats.clear()
        dt_wdw.destroy()
    
    tk.Button(dt_wdw, text="Confirm Payment", bg="green", fg="white",
              font=("Arial", 12, "bold"), command=confirm_payment).pack(pady=20)

for row in rows_top:
    for num in range(1, 9):  
        seat_map[f"{row}{num}"] = False
for row in rows_bottom:
    for num in range(1, 11):  
        seat_map[f"{row}{num}"] = False



root = tk.Tk()
root.title("Cinema Seat Booking")
root.geometry("1000x650")

#header
header_pg = tk.Label(root, text="🎬 Cinema Seat Booking System",
                 font=("Arial", 18, "bold"), fg="white", bg="grey")
header_pg.pack(pady=10)

#the screen in front
screen = tk.Label (root, text="[----------------------------------------------------]",font="black", width=30, height=2)
screen.pack(pady=10)

seat_frame = tk.Frame(root)
seat_frame.pack(pady=20)

for r, row in enumerate(rows_top): # as a list
    tk.Label(seat_frame, text=row,font=("Arial", 12, "bold")).grid(row=r, column=0, padx=10)

    for c in range(1, 9): # draw the seat 1--8 based on their alphabets
        seat = f"{row}{c}"
        btn = tk.Button(seat_frame, text=str(c), width=4, height=2,
                        bg="green", fg="white", font=("Arial", 10, "bold"))
        btn.grid(row=r, column=c+1, padx=5, pady=5)  # shift +1 for centering
        btn.config(command=lambda s=seat, b=btn: choose_seat(s, b))
        seat_btn[seat] = btn
    tk.Label(seat_frame, text=row,font=("Arial", 12, "bold")).grid(row=r, column=10, padx=10)

#as the walk way between the top row and bottom row
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

tk.Button(root, text="Proceed to Payment", bg="blue", fg="white",
          font=("Arial", 14, "bold"), command=detail_pg).pack(pady=20)

root.mainloop()

