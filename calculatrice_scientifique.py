import math
import tkinter as tk
from tkinter import ttk

# Ity fonction ity dia ampiasaina activer ireo fonctions faharoa ao @ calculatrice
class CalculatriceScientifique:
    def __init__(self, parent):
        self.parent = parent
        self.expression = ""
        self.memoire = 0
        self.angle_mode = tk.StringVar(value="DEG")  

        self.create_ui()

    def second_func(self):
            """Active les fonctions secondaires"""
            pass

    # etw indray dia fanaovana interface principale izay hitahirizana ireo élément rehetra @ calculatrice
    def create_ui(self):
        main_frame = ttk.Frame(self.parent, padding=10)
        main_frame.pack(fill="both", expand=True)

        ecran_frame = ttk.LabelFrame(main_frame, text="Calculatrice Scientifique", padding=8)
        ecran_frame.pack(fill="x", pady=(0, 10))

        top_row = ttk.Frame(ecran_frame)
        top_row.pack(fill="x", pady=(0, 5))

        ttk.Label(top_row, text="Mode:").pack(side="left")
        ttk.Radiobutton(top_row, text="DEG", variable=self.angle_mode, value="DEG").pack(side="left", padx=5)
        ttk.Radiobutton(top_row, text="RAD", variable=self.angle_mode, value="RAD").pack(side="left", padx=5)

        ttk.Button(top_row, text="M+", command=self.memoire_plus, width=4).pack(side="right", padx=2)
        ttk.Button(top_row, text="MR", command=self.memoire_rappel, width=4).pack(side="right", padx=2)
        ttk.Button(top_row, text="MC", command=self.memoire_clear, width=4).pack(side="right", padx=2)

        self.display_var = tk.StringVar(value="0")
        self.entry = tk.Entry(
            ecran_frame,
            textvariable=self.display_var,
            font=("Consolas", 18, "bold"),
            justify="right",
            bd=2,
            relief="sunken"
        )
        self.entry.pack(fill="x", ipady=10)
        self.entry.bind("<Return>", lambda e: self.calculer())
        self.entry.bind("<Key>", self.on_key_press)

        self.historique_var = tk.StringVar(value="")
        ttk.Label(ecran_frame, textvariable=self.historique_var, font=("Consolas", 9), foreground="gray").pack(anchor="e")

        # Clavier
        clavier = ttk.Frame(main_frame)
        clavier.pack(fill="both", expand=True)

        # Définition des boutons [texte, commande, couleur]
        buttons = [
            [("2nd", lambda: self.basculer_second()), ("π", lambda: self.ajouter("pi")), ("e", lambda: self.ajouter("e")), ("C", self.clear), ("⌫", self.backspace)],
            [("x²", lambda: self.ajouter("**2")), ("1/x", lambda: self.ajouter("**(-1)")), ("|x|", lambda: self.ajouter_func("abs")), ("exp", lambda: self.ajouter_func("exp")), ("mod", lambda: self.ajouter("%"))],
            [("√x", lambda: self.ajouter_func("sqrt")), ("( ", lambda: self.ajouter("(")), (" )", lambda: self.ajouter(")")), ("n!", lambda: self.ajouter_func("factorial")), ("÷", lambda: self.ajouter("/"))],
            [("xʸ", lambda: self.ajouter("**")), ("7", lambda: self.ajouter("7")), ("8", lambda: self.ajouter("8")), ("9", lambda: self.ajouter("9")), ("×", lambda: self.ajouter("*"))],
            [("10ˣ", lambda: self.ajouter_func("10**")), ("4", lambda: self.ajouter("4")), ("5", lambda: self.ajouter("5")), ("6", lambda: self.ajouter("6")), ("−", lambda: self.ajouter("-"))],
            [("log", lambda: self.ajouter_func("log10")), ("1", lambda: self.ajouter("1")), ("2", lambda: self.ajouter("2")), ("3", lambda: self.ajouter("3")), ("+", lambda: self.ajouter("+"))],
            [("ln", lambda: self.ajouter_func("log")), ("+/-", self.plus_moins), ("0", lambda: self.ajouter("0")), (".", lambda: self.ajouter(".")), ("=", self.calculer)],
        ]

        # Boutons scientifiques 2eme ligne
        sci_buttons = [
            [("sin", lambda: self.ajouter_trig("sin")), ("cos", lambda: self.ajouter_trig("cos")), ("tan", lambda: self.ajouter_trig("tan"))],
            [("asin", lambda: self.ajouter_trig("asin")), ("acos", lambda: self.ajouter_trig("acos")), ("atan", lambda: self.ajouter_trig("atan"))],
        ]

        for r, row in enumerate(sci_buttons):
            f = ttk.Frame(clavier)
            f.pack(fill="x", pady=2)
            for c, (txt, cmd) in enumerate(row):
                ttk.Button(f, text=txt, command=cmd, width=8).pack(side="left", padx=2, expand=True, fill="x")

        # Séparateur
        ttk.Separator(clavier, orient="horizontal").pack(fill="x", pady=6)

        for r, row in enumerate(buttons):
            f = ttk.Frame(clavier)
            f.pack(fill="x", pady=2)
            for c, (txt, cmd) in enumerate(row):
                # style couleur pour = et C
                if txt == "=":
                    btn = tk.Button(f, text=txt, command=cmd, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), relief="raised", bd=2)
                elif txt == "C":
                    btn = tk.Button(f, text=txt, command=cmd, bg="#f44336", fg="white", font=("Arial", 11, "bold"), relief="raised", bd=2)
                else:
                    btn = ttk.Button(f, text=txt, command=cmd)
                
                if isinstance(btn, tk.Button):
                    btn.pack(side="left", padx=2, expand=True, fill="x", ipady=6)
                else:
                    btn.pack(side="left", padx=2, expand=True, fill="x")

    def ajouter(self, val):
        if self.display_var.get() == "0" and val not in [".", ")", "("]:
            self.expression = ""
        # Remplacer symboles visuels
        self.expression += val
        self.display_var.set(self.expression)

    def ajouter_func(self, func_name):
        # ex: sqrt -> sqrt(
        if func_name == "10**":
            self.ajouter("10**(")
        else:
            self.ajouter(f"{func_name}(")

    def ajouter_trig(self, func_name):
        self.ajouter(f"{func_name}(")

    def clear(self):
        self.expression = ""
        self.display_var.set("0")
        self.historique_var.set("")

    def backspace(self):
        self.expression = self.expression[:-1]
        self.display_var.set(self.expression if self.expression else "0")

    def plus_moins(self):
        try:
            # essaie d'inverser le dernier nombre
            if self.expression:
                # simple toggle sur expression entière si c'est un nombre
                val = self.evaluer_expression(self.expression)
                val = -val
                self.expression = str(val)
                self.display_var.set(self.expression)
        except:
            self.expression = f"-({self.expression})" if self.expression else "-"
            self.display_var.set(self.expression)

    def memoire_plus(self):
        try:
            self.memoire += self.evaluer_expression(self.display_var.get())
        except:
            pass

    def memoire_rappel(self):
        self.expression = str(self.memoire)
        self.display_var.set(self.expression)

    def memoire_clear(self):
        self.memoire = 0

    def on_key_press(self, event):
        # Permet taper direct au clavier
        if event.char in "0123456789+-*/().%":
            return
        if event.keysym in ("Return", "BackSpace"):
            return

    def evaluer_expression(self, expr):
        # Environnement sécurisé
        safe_dict = {
            "sin": lambda x: math.sin(math.radians(x)) if self.angle_mode.get() == "DEG" else math.sin(x),
            "cos": lambda x: math.cos(math.radians(x)) if self.angle_mode.get() == "DEG" else math.cos(x),
            "tan": lambda x: math.tan(math.radians(x)) if self.angle_mode.get() == "DEG" else math.tan(x),
            "asin": lambda x: math.degrees(math.asin(x)) if self.angle_mode.get() == "DEG" else math.asin(x),
            "acos": lambda x: math.degrees(math.acos(x)) if self.angle_mode.get() == "DEG" else math.acos(x),
            "atan": lambda x: math.degrees(math.atan(x)) if self.angle_mode.get() == "DEG" else math.atan(x),
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "abs": abs,
            "factorial": math.factorial,
            "pi": math.pi,
            "e": math.e,
        }

        # remplacer ^ par ** si jamais
        expr = expr.replace("^", "**")
        # remplacer symbole visuel
        expr = expr.replace("÷", "/").replace("×", "*").replace("−", "-")

        return eval(expr, {"__builtins__": {}}, safe_dict)

    def calculer(self):
        expr = self.display_var.get()
        if not expr or expr == "0":
            return
        try:
            resultat = self.evaluer_expression(expr)
            self.historique_var.set(f"{expr} =")
            # Formatage intelligent
            if isinstance(resultat, float):
                if resultat == int(resultat):
                    aff = str(int(resultat))
                else:
                    aff = f"{resultat:.10g}"
            else:
                aff = str(resultat)
            self.display_var.set(aff)
            self.expression = aff
        except ZeroDivisionError:
            self.display_var.set("Erreur: division par 0")
            self.expression = ""
        except Exception as e:
            self.display_var.set(f"Erreur: {e}")
            self.expression = ""
