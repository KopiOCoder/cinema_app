# app_tk.py
import tkinter as tk
from tkinter import messagebox, ttk
from utils import load_csv, inference

MOVIES_CSV = "movies.csv"  

def find_movie_by_title(movies, query):
    q = query.strip().lower()
    if not q:
        return None
    for m in movies:
        if m['title'].lower() == q:
            return m
    for m in movies:
        if q in m['title'].lower():
            return m
    return None

class SimpleRecommenderApp:
    def __init__(self, root):
        self.root = root
        root.title("Simple Movie Search (20 similar)")

        try:
            self.movies = load_csv(MOVIES_CSV)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find {MOVIES_CSV}")
            root.destroy()
            return

        frm = ttk.Frame(root, padding=10)
        frm.grid(row=0, column=0, sticky="ew")
        frm.columnconfigure(1, weight=1)

        ttk.Label(frm, text="Movie title:").grid(row=0, column=0, sticky="w")
        self.entry = ttk.Entry(frm)
        self.entry.grid(row=0, column=1, sticky="ew", padx=(6,0))
        self.entry.bind("<Return>", lambda e: self.search())

        self.search_btn = ttk.Button(frm, text="Search", command=self.search)
        self.search_btn.grid(row=0, column=2, padx=(6,0))

        self.target_label = ttk.Label(root, text="Target: —", padding=(10,6,10,0))
        self.target_label.grid(row=1, column=0, sticky="w")

        list_frame = ttk.Frame(root, padding=10)
        list_frame.grid(row=2, column=0, sticky="nsew")
        root.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(list_frame, height=20)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

    def search(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showinfo("Info", "Type a movie title (or part of it) and click Search.")
            return

        movie = find_movie_by_title(self.movies, query)
        if movie is None:
            messagebox.showinfo("Not found", "No movie matched that title.")
            return

        results = inference(self.movies, movie['id'])
        if results is None:
            messagebox.showerror("Error", "Failed to compute similarities for this movie.")
            return

        self.target_label.config(text=f"Target: {results['target_title']}")
        self.listbox.delete(0, tk.END)

        similar = results.get('similar_movies', [])
        if not similar:
            self.listbox.insert(tk.END, "No similar movies found.")
            return

        for i, item in enumerate(similar, start=1):
            line = f"{i:2d}. {item['title']}  —  sim: {item['similarity']:.3f}"
            self.listbox.insert(tk.END, line)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleRecommenderApp(root)
    root.geometry("640x480")
    root.mainloop()