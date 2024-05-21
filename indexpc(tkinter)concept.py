import tkinter as tk
import json

class ShoppingCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Cart")
        self.root.configure(bg='black')

        # Cargamos los productos desde un archivo JSON
        self.load_products()

        # Diccionario para almacenar las variables de cantidad por producto
        self.quantities = {}

        self.build_ui()

    def load_products(self):
        try:
            with open('products.json', 'r') as file:
                self.sections = json.load(file)
        except FileNotFoundError:
            self.sections = {"Bebidas": [], "Dulce": [], "Salado": []}

    def build_ui(self):
        row = 0
        for section, products in self.sections.items():
            self.create_section_header(section, row)
            row += 1
            for product_name, price in products:
                self.create_product_widgets(product_name, price, row)
                row += 1

        # Botón Clear
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_quantities, bg="red", fg="white", font=("Helvetica", 12, "bold"), bd=0)
        self.clear_button.grid(row=row, columnspan=5, pady=10, padx=10, sticky="ew")

        row += 1
        # Etiqueta para mostrar el precio total
        self.total_label = tk.Label(self.root, text="Total: $0", font=("Helvetica", 14, "bold"), fg="white", bg="black")
        self.total_label.grid(row=row, columnspan=5, pady=10)

        # Actualizamos el total inicialmente
        self.update_total()

    def create_section_header(self, section_name, row):
        header = tk.Label(self.root, text=section_name, bg="purple", fg="white", font=("Helvetica", 16, "bold"))
        header.grid(row=row, columnspan=5, sticky="ew")

    def create_product_widgets(self, product_name, price, row):
        tk.Label(self.root, text=product_name, font=("Helvetica", 12), anchor="w", fg="white", bg="black").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self.root, text=f"${price}", font=("Helvetica", 12), fg="white", bg="black").grid(row=row, column=1, padx=10, pady=5)

        # Inicializamos la cantidad a 0
        self.quantities[product_name] = tk.IntVar(value=0)

        # Botones de incremento y decremento
        tk.Button(self.root, text="-", command=lambda p=product_name: self.update_quantity(p, -1), bg="gray", fg="white", font=("Helvetica", 12), bd=0).grid(row=row, column=2, padx=5)
        tk.Label(self.root, textvariable=self.quantities[product_name], font=("Helvetica", 12), fg="white", bg="black").grid(row=row, column=3, padx=5)
        tk.Button(self.root, text="+", command=lambda p=product_name: self.update_quantity(p, 1), bg="gray", fg="white", font=("Helvetica", 12), bd=0).grid(row=row, column=4, padx=5)

    def update_quantity(self, product_name, change):
        new_quantity = self.quantities[product_name].get() + change
        if new_quantity >= 0:
            self.quantities[product_name].set(new_quantity)
            self.update_total()

    def update_total(self):
        total = sum(q.get() * price for section in self.sections.values() for product, price in section for q in [self.quantities[product]])
        self.total_label.config(text=f"Total: ${total}")

    def clear_quantities(self):
        for product_name in self.quantities:
            self.quantities[product_name].set(0)
        self.update_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCartApp(root)
    root.mainloop()
