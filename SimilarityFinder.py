# app.py
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from utils import load_csv, inference

MOVIES_CSV = "movies.csv"

def show_app_page(parent):
    """
    Swaps out parent._main_frame and replaces it with the movie-recommender UI.
    Returns the new frame so you could keep a reference if you like.
    """
    # 1) hide the existing main page
    main = getattr(parent, "_main_frame", None)
    if main:
        main.pack_forget()

    # 2) build a new CTkFrame to host the recommender
    app_frame = ctk.CTkFrame(parent, corner_radius=15)
    app_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # --- Header ---
    header = ctk.CTkLabel(
        app_frame,
        text="Movie Recommender",
        font=("Arial", 24, "bold")
    )
    header.pack(pady=(0, 20))

    # --- Search row ---
    search_row = ctk.CTkFrame(app_frame)
    search_row.pack(fill="x", pady=(0, 10))
    search_row.columnconfigure(1, weight=1)

    ctk.CTkLabel(search_row, text="Movie title:").grid(row=0, column=0, sticky="w")
    entry = ctk.CTkEntry(search_row)
    entry.grid(row=0, column=1, sticky="ew", padx=(8, 8))
    search_btn = ctk.CTkButton(search_row, text="Search")
    search_btn.grid(row=0, column=2)

    target_label = ctk.CTkLabel(app_frame, text="Target: —", font=("Arial", 14))
    target_label.pack(anchor="w", pady=(0, 10))

    # --- Results list ---
    list_container = tk.Frame(app_frame)
    list_container.pack(fill="both", expand=True, pady=(0, 20))
    listbox = tk.Listbox(list_container, height=12)
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(list_container, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    # --- Load movies once ---
    try:
        movies = load_csv(MOVIES_CSV)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Could not find {MOVIES_CSV}")
        movies = []

    def find_movie_by_title(query):
        q = query.strip().lower()
        if not q:
            return None
        # exact match
        for m in movies:
            if m["title"].lower() == q:
                return m
        # partial
        for m in movies:
            if q in m["title"].lower():
                return m
        return None

    # --- Search logic ---
    def do_search(_evt=None):
        q = entry.get().strip()
        if not q:
            messagebox.showinfo("Info", "Type a movie title and click Search.")
            return

        m = find_movie_by_title(q)
        if not m:
            messagebox.showinfo("Not found", "No movie matched that title.")
            return

        results = inference(movies, m["id"])
        if not results:
            messagebox.showerror("Error", "Failed to compute similarities.")
            return

        target_label.configure(text=f"Target: {results['target_title']}")
        listbox.delete(0, tk.END)

        sims = results.get("similar_movies", [])
        if not sims:
            listbox.insert(tk.END, "No similar movies found.")
            return

        for i, item in enumerate(sims, start=1):
            line = f"{i:2d}. {item['title']}  —  sim: {item['similarity']:.3f}"
            listbox.insert(tk.END, line)

    entry.bind("<Return>", do_search)
    search_btn.configure(command=do_search)

    # Return the frame in case caller wants to hold it
    return app_frame
