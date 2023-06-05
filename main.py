import tkinter as tk
from tkinter import filedialog
from tkinter import font

import algoritmos as a

class TextEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Subasta pública de acciones")
        self.master.geometry("625x450")
        self.master.configure(bg ="#ced0ce")
        self.create_widgets()
        self.file_path = None

    def create_widgets(self):
        # Caja de texto donde se muestra el archivo
        fuente = font.Font(family="Roboto", size=12)
        self.entrada = tk.Text(self.master, height=20, width=25,state="disabled", bg="#ced0ce", font=fuente)
        self.entrada.grid(column=0, row=0, padx=10, pady=10)

        # Caja de texto donde se muestra la solución
        fuente = font.Font(family="Roboto", size=12)
        self.solucion = tk.Text(self.master, height=20, width=25,state="disabled", bg="#ced0ce", font=fuente)
        self.solucion.grid(column=1, row=0, padx=10, pady=10)

        # Botón para "subir" un archivo
        self.open_button = tk.Button(self.master, text="Abrir archivo", command=self.open_file, font=fuente)
        self.open_button.grid(column=2, row=0, padx=10, pady=10)

        # Botones para escribir el archivo de salida
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
        self.buttons_frame.config(bg="#ced0ce")

        self.button_a = tk.Button(self.buttons_frame, text="Fuerza bruta", command=lambda: self.write_to_file("A"), font=fuente)
        self.button_a.pack(side="left", padx=5, pady=5)

        self.button_b = tk.Button(self.buttons_frame, text="Voraz", command=lambda: self.write_to_file("B"), font=fuente)
        self.button_b.pack(side="left", padx=5, pady=5)

        self.button_c = tk.Button(self.buttons_frame, text="Dinámica 1", command=lambda: self.write_to_file("C"), font=fuente)
        self.button_c.pack(side="left", padx=5, pady=5)

        self.button_d = tk.Button(self.buttons_frame, text="Dinámica 2", command=lambda: self.write_to_file("D"), font=fuente)
        self.button_d.pack(side="left", padx=5, pady=5)

    #Abre el archivo y lo muestra en la caja
    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            with open(self.file_path, "r") as f:
                text = f.read()
                self.entrada.config(state="normal")
                self.entrada.delete("1.0", tk.END)
                self.entrada.insert(tk.END, text)
                self.entrada.config(state="disabled")

    #Abre un diálogo para guardar el archivo, lo escribe y muestra en la caja
    def write_to_file(self, opcion):
        entrada = self.file_path
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt")])
        if opcion == "A":
          resultado = a.accionesFB(entrada)
        elif opcion == "B":
          resultado = a.accionesV(entrada)
        elif opcion == "C":
          resultado = a.accionesPD1(entrada)
        elif opcion == "D":
          resultado = a.accionesPD2(entrada)
        if file_path:
            with open(file_path, "w") as f:
                f.write(resultado)
                self.solucion.config(state="normal")
                self.solucion.delete("1.0", tk.END)
                self.solucion.insert(tk.END, resultado)
                self.solucion.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
