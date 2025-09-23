import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image, ImageTk


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
	messagebox.showinfo("Selected", f"You selected: {selected['title']}")
	import subprocess
	subprocess.Popen(["python", "seat.py", selected['title']])
	# Here, you can call seat booking logic and pass selected movie info


def auto_rotate():
	if carousel_running:
		next_movie()
		root.after(3000, auto_rotate)

# --- UI Setup ---
root = ctk.CTk()
root.title("Cinema Kiosk App")
root.geometry("800x600")

carousel_frame = ctk.CTkFrame(root, width=350, height=260, corner_radius=15)
carousel_frame.pack(pady=40)

image_label = ctk.CTkLabel(carousel_frame, text="", width=300, height=180)
image_label.pack(pady=(20, 10))
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

btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=10)

prev_btn = ctk.CTkButton(btn_frame, text="\u25C0", command=prev_movie, width=60, font=("Arial", 24))
prev_btn.grid(row=0, column=0, padx=10)

next_btn = ctk.CTkButton(btn_frame, text="\u25B6", command=next_movie, width=60, font=("Arial", 24))
next_btn.grid(row=0, column=2, padx=10)

show_movie(current_index)
root.after(3000, auto_rotate)
root.mainloop()



