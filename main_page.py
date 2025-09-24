import customtkinter as ctk
import os
from PIL import Image, ImageTk
from seat import show_seat_page
from Fud  import show_food_page
from app  import show_app_page

# --- Movie Data & Carousel Helpers (unchanged) ---
movies = [
    {"title": "Avengers: Endgame", "image": "photos/advengers.webp"},
    {"title": "Spiderman: Into the Spider-Verse", "image": "photos/spiderman.jpg"},
    {"title": "Superman: Legacy", "image": "photos/superman.jpg"}
]
current_index    = 0
carousel_running = True

def load_image(path, size=(300, 400)):
    if not os.path.exists(path):
        img = Image.new("RGB", size, color="#333")
        return ImageTk.PhotoImage(img)
    img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def show_movie(index):
    m = movies[index]
    title_label.configure(text=m["title"])
    img = load_image(m["image"])
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

def auto_rotate():
    if carousel_running:
        next_movie()
        root.after(3000, auto_rotate)
        
def select_movie(event=None):
    main_frame.pack_forget()
    show_seat_page(root, movies[current_index]["title"])

def highlight(tab_key):
    for key, btn in tabs.items():
        btn.configure(fg_color=inactive_bg)
    tabs[tab_key].configure(fg_color=active_bg)

# --- Frame‐swap callbacks ---
def on_movies():
    highlight("movies")
    sim_frame.pack_forget()
    food_frame.pack_forget()
    main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

def on_food():
    highlight("food")
    sim_frame.pack_forget()
    main_frame.pack_forget()
    food_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

def on_similarity():
    highlight("sim")
    main_frame.pack_forget()
    food_frame.pack_forget()
    sim_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# --- App setup ---
root = ctk.CTk()
root.title("Cinema Kiosk App")
root.geometry("1200x700")

# 1) Sidebar
sidebar = ctk.CTkFrame(root, width=100)
sidebar.pack(side="left", fill="y")

active_bg = "#1f6aa5"
inactive_bg = sidebar.cget("fg_color")

tabs = {}
tabs["movies"] = ctk.CTkButton(
    sidebar, text="🎬\nMovies", fg_color=inactive_bg,
    hover_color="#555", width=80, height=80, command=on_movies
)
tabs["food"]    = ctk.CTkButton(
    sidebar, text="🍔\nFood", fg_color=inactive_bg,
    hover_color="#555", width=80, height=80, command=on_food
)
tabs["sim"]     = ctk.CTkButton(
    sidebar, text="🔍\nSimilarity", fg_color=inactive_bg,
    hover_color="#555", width=80, height=80, command=on_similarity
)

for btn in tabs.values():
    btn.pack(fill="x", expand=True, pady=10)

# 2) Main movie carousel frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
root._main_frame = main_frame

carousel_frame = ctk.CTkFrame(main_frame, width=350, height=450, corner_radius=15)
carousel_frame.pack(pady=40)
carousel_frame.pack_propagate(False)

image_label = ctk.CTkLabel(carousel_frame, text="", width=300, height=400)
image_label.pack()
image_label.bind("<Button-1>", select_movie)

title_label = ctk.CTkLabel(carousel_frame, text="", font=("Arial", 18, "bold"))
title_label.pack(pady=5)

btn_nav = ctk.CTkFrame(main_frame)
btn_nav.pack(pady=10)
ctk.CTkButton(btn_nav, text="◀", command=prev_movie, width=60,  font=("Arial",24)).grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_nav, text="▶", command=next_movie, width=60,  font=("Arial",24)).grid(row=0, column=1, padx=10)

image_label.bind("<Enter>", lambda e: image_label.configure(
    image=load_image(movies[current_index]["image"], (350,450)),
    ))
image_label.bind("<Leave>", lambda e: image_label.configure(
    image=load_image(movies[current_index]["image"], (300,400))
    ))

show_movie(current_index)
root.after(3000, auto_rotate)

# 3) Pre‐build one similarity frame
sim_frame = ctk.CTkFrame(root)
food_frame = ctk.CTkFrame(root)  # if you had a prebuilt food_frame do the same trick there
# don't pack it yet!
# fill it only once
show_app_page(sim_frame)
show_food_page(food_frame)  # just to test; remove this line

highlight("movies")

root.mainloop()
