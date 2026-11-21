import random
import tkinter as tk

try:
    from rows import rows
except ImportError:
    # Si no está rows.py, arranca con datos de prueba
    rows = [[random.randint(0, 3) for _ in range(15)] for _ in range(17)]

cantFilas = len(rows)
cantColumnas = len(rows[0])
TAM_CELDA = 20          # tamaño de cada celda en píxeles
INTERVALO_MS = 200      # cada cuánto se actualiza (0.5 s)

# Colores base de la paleta (de valor bajo a alto)
ANCLAS = [
    "#ffffff", "#e2d497", "#e7c366", "#ffba08", "#faa307", "#f48c06", "#e85d04",
    "#dc2f02", "#d00000", "#9d0208", "#6a040f", "#370617", "#1e0303", "#000000",
]
PASOS = 3   # cuántos colores hay entre un color base y el siguiente (1 = solo los base)


def generar_paleta(anclas, pasos):
    """Interpola 'pasos' colores entre cada par de colores base."""
    def a_rgb(h):
        return [int(h[k:k + 2], 16) for k in (1, 3, 5)]

    paleta = []
    for c1, c2 in zip(anclas, anclas[1:]):
        a, b = a_rgb(c1), a_rgb(c2)
        for p in range(pasos):
            t = p / pasos
            r, g, bl = (round(a[k] + (b[k] - a[k]) * t) for k in range(3))
            paleta.append(f"#{r:02x}{g:02x}{bl:02x}")
    paleta.append(anclas[-1])
    return paleta


# Un color por valor: COLORES[0] para 0, COLORES[1] para 1, ... el último para ese valor o más
COLORES = generar_paleta(ANCLAS, PASOS)


def cambiar_color(rows):
    for i in range(1, cantFilas):
        actual = rows[i]
        anterior = rows[i - 1]
        for j in range(cantColumnas):
            actual[j] = anterior[j] + random.randint(0, 3)


def valor_a_color(valor):
    # Recorta a los extremos: menos de 0 -> primer color, más de 13 -> último
    indice = max(0, min(int(valor), len(COLORES) - 1))
    return COLORES[indice]


class App:
    def __init__(self, root):
        self.root = root
        root.title("Grilla de colores")
        self.canvas = tk.Canvas(root, width=cantColumnas * TAM_CELDA,
                                height=cantFilas * TAM_CELDA,
                                bg="black", highlightthickness=0)
        self.canvas.pack()

        # Crear las celdas una sola vez; la fila 0 se dibuja abajo
        self.celdas = []
        for i in range(cantFilas):
            y0 = (cantFilas - 1 - i) * TAM_CELDA
            fila = []
            for j in range(cantColumnas):
                x0 = j * TAM_CELDA
                fila.append(self.canvas.create_rectangle(
                    x0, y0, x0 + TAM_CELDA, y0 + TAM_CELDA, outline=""))
            self.celdas.append(fila)

        self.actualizar()

    def actualizar(self):
        cambiar_color(rows)
        for i in range(cantFilas):
            for j in range(cantColumnas):
                self.canvas.itemconfig(self.celdas[i][j],
                                       fill=valor_a_color(rows[i][j]))
        self.root.after(INTERVALO_MS, self.actualizar)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()