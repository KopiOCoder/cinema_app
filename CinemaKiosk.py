import customtkinter as ctk
import os
from PIL import Image, ImageTk
from seat import show_seat_page
from Food import show_food_page
from SimilarityFinder import show_app_page

# --- Movie Data & Carousel Helpers (unchanged) ---
movies = [
    {"title": "Avengers: Endgame", "image": "photos/advengers.webp"},
    {"title": "Spiderman: Into the Spider-Verse", "image": "photos/spiderman.jpg"},
    {"title": "Superman: Legacy", "image": "photos/superman.jpg"}
]
current_index = 0
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

# --- App setup ---
root = ctk.CTk()
root.title("Cinema Kiosk App")
root.geometry("1200x700")

# 1) Create a dict of all your pages
frames = {}

frames["main"] = ctk.CTkFrame(root)
frames["food"] = ctk.CTkFrame(root)
frames["sim"] = ctk.CTkFrame(root)


# 2) Helper to show exactly one frame at a time
def show_frame(key):
    # Hide whatever’s on screen
    for f in list(frames.values()):
        f.pack_forget()
    
    # If this is a seat‐page, tear down + rebuild
    if key.startswith("seat"):
        idx = int(key[len("seat"):])      # e.g. "seat1" → 1
        # destroy old if it exists
        old = frames.get(key)
        if old is not None:
            old.destroy()
        # build a fresh frame & hook it into frames
        new = ctk.CTkFrame(root)
        show_seat_page(new, movies[idx]["title"])
        frames[key] = new

    # Pack the requested frame
    frames[key].pack(side="left", fill="both", expand=True, padx=20, pady=20)
root.show_frame = show_frame

# 3) Sidebar & Tab Buttons
sidebar = ctk.CTkFrame(root, width=100)
sidebar.pack(side="left", fill="y")

active_bg = "#1f6aa5"
inactive_bg = "#616161"
hover_bg = "#5477d1"

def highlight(key):
    for k, btn in tabs.items():
        btn.configure(fg_color=inactive_bg)
    tabs[key].configure(fg_color=active_bg)

def on_movies():
    highlight("movies")
    show_frame("main")

def on_food():
    highlight("food")
    show_frame("food")

def on_similarity():
    highlight("sim")
    show_frame("sim")

tabs = {
    "movies": ctk.CTkButton(
        sidebar, text="🎬\nMovies", fg_color=inactive_bg,
        hover_color=hover_bg, width=80, height=80,
        command=on_movies
    ),
    "food": ctk.CTkButton(
        sidebar, text="🍔\nFood", fg_color=inactive_bg,
        hover_color=hover_bg, width=80, height=80,
        command=on_food
    ),
    "sim": ctk.CTkButton(
        sidebar, text="🔍\nSimilarity", fg_color=inactive_bg,
        hover_color=hover_bg, width=80, height=80,
        command=on_similarity
    )
}

for btn in tabs.values():
    btn.pack(fill="x", expand=True, pady=10)

# 4) Build Main Movie Carousel inside frames["main"]
main_frame = frames["main"]
main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

carousel_frame = ctk.CTkFrame(main_frame, width=350, height=450, corner_radius=15)
carousel_frame.pack(pady=40)
carousel_frame.pack_propagate(False)

image_label = ctk.CTkLabel(carousel_frame, text="", width=300, height=400)
image_label.pack()
image_label.bind(
    "<Button-1>",
    lambda e: show_frame(f"seat{current_index}")
)

title_label = ctk.CTkLabel(carousel_frame, text="", font=("Arial", 18, "bold"))
title_label.pack(pady=5)

btn_nav = ctk.CTkFrame(main_frame)
btn_nav.pack(pady=10)
ctk.CTkButton(btn_nav, text="◀", command=prev_movie, width=60,  font=("Arial",24)).grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_nav, text="▶", command=next_movie, width=60,  font=("Arial",24)).grid(row=0, column=1, padx=10)

image_label.bind("<Enter>", lambda e: image_label.configure(
    image=load_image(movies[current_index]["image"], (350,450))
))
image_label.bind("<Leave>", lambda e: image_label.configure(
    image=load_image(movies[current_index]["image"], (300,400))
))

show_movie(current_index)
root.after(3000, auto_rotate)

# 5) Pre‐build similarity & food pages
show_app_page(frames["sim"])
show_food_page(frames["food"])

# 6) Initialize on the Movies tab
highlight("movies")
show_frame("main")

root.mainloop()
