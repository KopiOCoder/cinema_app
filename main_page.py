import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from seat import show_seat_page
from Fud import show_food_page

# --- Movie Data ---
movies = [
	{"title": "Avengers: Endgame", "image": "photos/advengers.webp"},
	{"title": "Spiderman: Into the Spider-Verse", "image": "photos/spiderman.jpg"},
	{"title": "Superman: Legacy", "image": "photos/superman.jpg"}
]

current_index = 0
carousel_running = True

def load_image(path, size=(300, 400)):
	if not os.path.exists(path):
		# Placeholder if image not found
		img = Image.new("RGB", size, color="#333")
		return ImageTk.PhotoImage(img)
	img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
	return ImageTk.PhotoImage(img)

def show_movie(index):
	movie = movies[index]
	title_label.configure(text=movie["title"])
	img = load_image(movie["image"])
	image_label.configure(image=img)
	image_label.image = img

def next_movie():
	global current_index
	current_index = (current_index + 1) % len(movies)
	show_movie(current_index)

def prev_movie():
	global current_index
	current_index = (current_index - 1) % len(movies)
	show_movie(current_index)

def select_movie():
    selected = movies[current_index]
    # hide the whole main area
    root._main_frame.pack_forget()
    show_seat_page(root, selected['title'])

def select_food():
	root._main_frame.pack_forget()
	show_food_page(root, checkout_callback=None, json_path="FoodDrinks.json")

def auto_rotate():
	if carousel_running:
		next_movie()
		root.after(3000, auto_rotate)

# --- UI Setup ---
root = ctk.CTk()
root.title("Cinema Kiosk App")
root.geometry("1200x700")

main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, pady=20)
root._main_frame = main_frame   # store reference for seat page to restore

carousel_frame = ctk.CTkFrame(main_frame, width=350, height=450, corner_radius=15)
carousel_frame.pack(pady=40)
carousel_frame.pack_propagate(False)

image_label = ctk.CTkLabel(carousel_frame, text="", width=300, height=400)
image_label.pack(pady=(0, 0))
image_label.bind("<Button-1>", lambda event: select_movie())

# --- Hover effect ---
def on_image_enter(event):
	movie = movies[current_index]
	img = load_image(movie["image"], size=(350, 450))
	image_label.configure(image=img)
	image_label.image = img

def on_image_leave(event):
	movie = movies[current_index]
	img = load_image(movie["image"], size=(300, 400))
	image_label.configure(image=img)
	image_label.image = img

image_label.bind("<Enter>", on_image_enter)
image_label.bind("<Leave>", on_image_leave)

title_label = ctk.CTkLabel(carousel_frame, text="", font=("Arial", 18, "bold"))
title_label.pack(pady=5)

btn_frame = ctk.CTkFrame(main_frame)
btn_frame.pack(pady=10)

prev_btn = ctk.CTkButton(btn_frame, text="\u25C0", command=prev_movie, width=60, font=("Arial", 24))
prev_btn.grid(row=0, column=0, padx=10)

next_btn = ctk.CTkButton(btn_frame, text="\u25B6", command=next_movie, width=60, font=("Arial", 24))
next_btn.grid(row=0, column=2, padx=10)

btn2_frame = ctk.CTkFrame(main_frame)
btn2_frame.pack(pady=10)

food_btn = ctk.CTkButton(btn2_frame, text="Order Food", command=lambda: select_food(), width=200, height=50, font=("Arial", 18))
food_btn.grid(row=0, column=0, padx=10)

show_movie(current_index)
root.after(3000, auto_rotate)
root.mainloop()



