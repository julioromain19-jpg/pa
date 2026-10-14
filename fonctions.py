import math

FONCTIONS = {
    "Affine": {
        "formula": "f(x) = ax + b",
        "params": [
            ("a", "coefficient directeur", 2),
            ("b", "ordonnée à l'origine", 1)
        ]
    },
    "Linéaire": {
        "formula": "f(x) = ax",
        "params": [
            ("a", "coefficient", 2)
        ]
    },
    "Polynôme": {
        "formula": "f(x) = ax² + bx + c",
        "params": [
            ("a", "coefficient de x²", 1),
            ("b", "coefficient de x", 0),
            ("c", "constante", -1)
        ]
    },
    "Puissance": {
        "formula": "f(x) = a × xⁿ",
        "params": [
            ("a", "coefficient", 1),
            ("n", "exposant", 2)
        ]
    },
    "Exponentielle": {
        "formula": "f(x) = a × bˣ",
        "params": [
            ("a", "coefficient", 1),
            ("b", "base (b > 0, b ≠ 1)", 2)
        ]
    },
    "Logarithme": {
        "formula": "f(x) = a × log_b(x)",
        "params": [
            ("a", "coefficient", 1),
            ("b", "base (b > 0, b ≠ 1)", 2)
        ]
    }
}

def analyser_fonction(nom, p):
    if nom == "Affine":
        a, b = p["a"], p["b"]

        def f(x):
            return a*x+b

        zero = None if a == 0 else -b/a
        details = (
            "FONCTION AFFINE\n\n"
            f"Forme : f(x) = {a:g}x + {b:g}\n"
            f"Coefficient directeur a = {a:g}\n"
            f"Ordonnée à l'origine b = {b:g}\n"
            f"f(0) = {b:g}\n"
        )
        if a != 0:
            details += f"Zéro : x = {zero:g}\n"
            details += "Variation : croissante\n" if a > 0 else "Variation : décroissante\n"
        else:
            details += "Fonction constante.\n"

        return {"fonction": f, "details": details}

    if nom == "Linéaire":
        a = p["a"]

        def f(x):
            return a*x

        details = (
            "FONCTION LINÉAIRE\n\n"
            f"Forme : f(x) = {a:g}x\n"
            f"Coefficient a = {a:g}\n"
            "Zéro : x = 0\n"
        )
        if a > 0:
            details += "Variation : croissante\n"
        elif a < 0:
            details += "Variation : décroissante\n"
        else:
            details += "Fonction nulle.\n"

        return {"fonction": f, "details": details}

    if nom == "Polynôme":
        a, b, c = p["a"], p["b"], p["c"]

        if a == 0:
            # Cas dégénéré : devient affine
            return analyser_fonction("Affine", {"a": b, "b": c})

        def f(x):
            return a*x*x+b*x+c

        delta = b*b - 4*a*c
        details = (
            "POLYNÔME DU SECOND DEGRÉ\n\n"
            f"Forme : f(x) = {a:g}x² + {b:g}x + {c:g}\n"
            f"Δ = b² - 4ac = {delta:g}\n"
        )

        if delta > 0:
            x1 = (-b-math.sqrt(delta))/(2*a)
            x2 = (-b+math.sqrt(delta))/(2*a)
            details += f"Deux racines réelles :\n x₁ = {x1:g}\n x₂ = {x2:g}\n"
        elif delta == 0:
            x0 = -b/(2*a)
            details += f"Une racine double : x₀ = {x0:g}\n"
        else:
            details += "Aucune racine réelle.\n"

        xs = -b/(2*a)
        ys = f(xs)
        details += f"Sommet : S({xs:g} ; {ys:g})\n"
        details += "Parabole tournée vers le haut.\n" if a > 0 else "Parabole tournée vers le bas.\n"

        return {"fonction": f, "details": details}

    if nom == "Puissance":
        a, n = p["a"], p["n"]

        def f(x):
            if x < 0 and not float(n).is_integer():
                return float("nan")
            return a*(x**n)

        details = (
            "FONCTION PUISSANCE\n\n"
            f"Forme : f(x) = {a:g} × x^{n:g}\n"
            f"Coefficient a = {a:g}\n"
            f"Exposant n = {n:g}\n"
        )
        if n == 0:
            details += "Fonction constante sur son domaine.\n"
        elif n > 0:
            details += "Domaine général : x ≥ 0 pour l'affichage réel si n n'est pas entier.\n"

        return {"fonction": f, "details": details}

    if nom == "Exponentielle":
        a, b = p["a"], p["b"]

        if b <= 0 or b == 1:
            raise ValueError("La base b doit être > 0 et différente de 1.")

        def f(x):
            return a*(b**x)

        details = (
            "FONCTION EXPONENTIELLE\n\n"
            f"Forme : f(x) = {a:g} × {b:g}ˣ\n"
            f"a = {a:g}\n"
            f"b = {b:g}\n"
            f"f(0) = {a:g}\n"
        )
        details += "Variation : croissante.\n" if b > 1 else "Variation : décroissante.\n"
        details += "La fonction ne s'annule pas si a ≠ 0.\n"

        return {"fonction": f, "details": details}

    if nom == "Logarithme":
        a, b = p["a"], p["b"]

        if b <= 0 or b == 1:
            raise ValueError("La base b doit être > 0 et différente de 1.")

        def f(x):
            if x <= 0:
                return float("nan")
            return a*math.log(x, b)

        details = (
            "FONCTION LOGARITHME\n\n"
            f"Forme : f(x) = {a:g} × log_{b:g}(x)\n"
            f"a = {a:g}\n"
            f"b = {b:g}\n"
            "Domaine : x > 0\n"
            "Zéro : x = 1\n"
        )
        details += "Variation : croissante.\n" if a > 0 and b > 1 else "La variation dépend des signes de a et de ln(b).\n"

        return {"fonction": f, "details": details}

    raise ValueError("Fonction inconnue.")


