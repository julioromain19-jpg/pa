import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from fonctions import analyser_fonction, FONCTIONS
from calculatrice_scientifique import CalculatriceScientifique

# Classe ngaza miandraikitra interface graphique an'ilay module Résolveur de Fonctions
class ResolveurFrame:
    def __init__(self, parent):
        self.parent = parent
        self.entries = {}
        self.current_result = None
        self.create_ui()
        self.update_fields()

     #ity def create_ui dia mamorona ny interface graphique manontolo ho an'ny Résolveur de Fonctions
    def create_ui(self):
        header = ttk.Frame(self.parent, padding=(18, 14))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="RÉSOLVEUR DE FONCTIONS",
            font=("Arial", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Calcul • Analyse • Tableau de valeurs • Courbe",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(3, 0))

        main = ttk.PanedWindow(self.parent, orient="horizontal")
        main.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        left = ttk.Frame(main, padding=12)
        right = ttk.Frame(main, padding=8)
        main.add(left, weight=0)
        main.add(right, weight=1)

        # etw indray manao karazana table asiana any titre "Type de fonction"
        selection = ttk.LabelFrame(left, text="1. Type de fonction", padding=12)
        selection.pack(fill="x", pady=(0, 10))

        self.function_var = tk.StringVar(value="Affine")
        self.function_box = ttk.Combobox(
            selection,
            textvariable=self.function_var,
            values=list(FONCTIONS.keys()),
            state="readonly",
            width=25
        )
        self.function_box.pack(fill="x")
        self.function_box.bind("<<ComboboxSelected>>", lambda e: self.update_fields())

        self.formula_label = ttk.Label(
            selection,
            text="",
            font=("Arial", 11, "italic")
        )
        self.formula_label.pack(anchor="w", pady=(12, 0))

        self.params_frame = ttk.LabelFrame(left, text="2. Paramètres", padding=12)
        self.params_frame.pack(fill="x", pady=(0, 10))

        
        interval = ttk.LabelFrame(left, text="3. Intervalle de la courbe", padding=12)
        interval.pack(fill="x", pady=(0, 10))

        row = ttk.Frame(interval)
        row.pack(fill="x")

        ttk.Label(row, text="X min").grid(row=0, column=0, padx=(0, 5))
        self.xmin = ttk.Entry(row, width=10)
        self.xmin.grid(row=0, column=1, padx=(0, 12))
        self.xmin.insert(0, "-10")

        ttk.Label(row, text="X max").grid(row=0, column=2, padx=(0, 5))
        self.xmax = ttk.Entry(row, width=10)
        self.xmax.grid(row=0, column=3)
        self.xmax.insert(0, "10")

        buttons = ttk.Frame(left)
        buttons.pack(fill="x", pady=4)

        ttk.Button(
            buttons, text="CALCULER",
            command=self.calculate
        ).pack(fill="x", pady=3)

        ttk.Button(
            buttons, text="RÉINITIALISER",
            command=self.reset
        ).pack(fill="x", pady=3)

        ttk.Button(
            buttons, text="ENREGISTRER LA COURBE",
            command=self.save_plot
        ).pack(fill="x", pady=3)

        # etw indray dia maneho ny place ny résultat azo rehefa manao calcul
        result_frame = ttk.LabelFrame(left, text="4. Résultats", padding=8)
        result_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(
            result_frame,
            wrap="word",
            font=("Consolas", 10),
            height=18
        )
        self.result_text.pack(fill="both", expand=True)

        graph_frame = ttk.LabelFrame(right, text="Courbe", padding=5)
        graph_frame.pack(fill="both", expand=True)

        self.fig, self.ax = plt.subplots(figsize=(7, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        toolbar.update()

        self.draw_empty()

    def update_fields(self):
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        self.entries.clear()
        name = self.function_var.get()
        data = FONCTIONS[name]

        self.formula_label.config(text=data["formula"])

        for i, (key, label, default) in enumerate(data["params"]):
            ttk.Label(
                self.params_frame,
                text=f"{key} :"
            ).grid(row=i, column=0, sticky="w", padx=(0, 8), pady=5)

            entry = ttk.Entry(self.params_frame, width=14)
            entry.grid(row=i, column=1, sticky="ew", pady=5)
            entry.insert(0, str(default))
            self.entries[key] = entry

            ttk.Label(
                self.params_frame,
                text=label
            ).grid(row=i, column=2, sticky="w", padx=(8, 0), pady=5)

        self.params_frame.columnconfigure(1, weight=1)

    def calculate(self):
        try:
            name = self.function_var.get()
            params = {k: float(v.get()) for k, v in self.entries.items()}
            xmin = float(self.xmin.get())
            xmax = float(self.xmax.get())

            if xmin >= xmax:
                raise ValueError("X min doit être inférieur à X max.")

            result = analyser_fonction(name, params)
            self.current_result = result

            self.show_results(result, xmin, xmax)
            self.draw_plot(result["fonction"], name, xmin, xmax)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def show_results(self, result, xmin, xmax):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result["details"])
        self.result_text.insert(
            tk.END,
            f"\n\nINTERVALLE DE TRACÉ\n"
            f"[{xmin:g} ; {xmax:g}]\n"
        )

        self.result_text.insert(tk.END, "\nTABLEAU DE VALEURS\n")
        self.result_text.insert(tk.END, "-" * 38 + "\n")
        self.result_text.insert(tk.END, f"{'x':>12} | {'f(x)':>15}\n")
        self.result_text.insert(tk.END, "-" * 38 + "\n")

        fn = result["fonction"]
        points = np.linspace(xmin, xmax, 11)

        for x in points:
            try:
                y = fn(x)
                if np.isfinite(y):
                    self.result_text.insert(
                        tk.END, f"{x:12.3f} | {y:15.5f}\n"
                    )
                else:
                    self.result_text.insert(
                        tk.END, f"{x:12.3f} | {'non défini':>15}\n"
                    )
            except:
                self.result_text.insert(
                    tk.END, f"{x:12.3f} | {'non défini':>15}\n"
                )

    def draw_empty(self):
        self.ax.clear()
        self.ax.set_title("Choisis une fonction puis clique sur CALCULER")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()

    def draw_plot(self, fn, name, xmin, xmax):
        x = np.linspace(xmin, xmax, 2000)
        y = np.full_like(x, np.nan, dtype=float)

        for i, value in enumerate(x):
            try:
                result = fn(value)
                if np.isfinite(result):
                    y[i] = result
            except:
                pass

        self.ax.clear()
        self.ax.plot(x, y, linewidth=2, label=name)
        self.ax.axhline(0, linewidth=0.8)
        self.ax.axvline(0, linewidth=0.8)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title(f"Courbe : {name}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def save_plot(self):
        path = filedialog.asksaveasfilename(
            title="Enregistrer la courbe",
            defaultextension=".png",
            filetypes=[("Image PNG", "*.png"), ("Image JPG", "*.jpg")]
        )

        if path:
            self.fig.savefig(path, dpi=200, bbox_inches="tight")
            messagebox.showinfo("Enregistrement", "La courbe a été enregistrée.")

    def reset(self):
        self.function_var.set("Affine")
        self.xmin.delete(0, tk.END)
        self.xmin.insert(0, "-10")
        self.xmax.delete(0, tk.END)
        self.xmax.insert(0, "10")
        self.update_fields()
        self.result_text.delete("1.0", tk.END)
        self.current_result = None
        self.draw_empty()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Résolveur + Calculatrice Scientifique - Version PRO")
        self.root.geometry("1350x850")
        self.root.minsize(1100, 750)

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            pass

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.tab_resolveur = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_resolveur, text="  📈 Résolveur de Fonctions  ")
        self.resolveur = ResolveurFrame(self.tab_resolveur)

        self.tab_calc = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_calc, text="  🔬 Calculatrice Scientifique  ")
        self.calc = CalculatriceScientifique(self.tab_calc)

        status = ttk.Frame(self.root, padding=(10, 5))
        status.pack(fill="x")
        ttk.Label(status, text="Astuce: Utilise sin(30), cos(45), sqrt(16), log(100), 2**3, pi, e, etc. | Mode DEG = degrés, RAD = radians", font=("Arial", 9), foreground="#555").pack(anchor="w")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
