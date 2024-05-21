import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class ProductEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Editor")

        # Cargamos los productos desde un archivo JSON
        self.load_products()

        self.build_ui()

    def load_products(self):
        try:
            with open('products.json', 'r') as file:
                self.sections = json.load(file)
        except FileNotFoundError:
            self.sections = {"Bebidas": [], "Salado": [], "Dulce": []}

    def save_products(self):
        with open('products.json', 'w') as file:
            json.dump(self.sections, file, indent=4)
        self.update_product_list()  # Clear the list after saving

    def build_ui(self):
        row = 0
        self.section_var = tk.StringVar(value="Bebidas")
        tk.Label(self.root, text="Sección:").grid(row=row, column=0)
        tk.OptionMenu(self.root, self.section_var, *self.sections.keys()).grid(row=row, column=1)

        row += 1
        tk.Button(self.root, text="Agregar Producto", command=self.add_product).grid(row=row, column=0, pady=10)
        tk.Button(self.root, text="Eliminar Producto", command=self.remove_product).grid(row=row, column=1, pady=10)
        tk.Button(self.root, text="Editar Precio", command=self.edit_price).grid(row=row, column=2, pady=10)

        row += 1
        tk.Button(self.root, text="Guardar Cambios", command=self.save_products).grid(row=row, columnspan=3, pady=10)

        row += 1
        self.product_list_label = tk.Label(self.root, text="Productos Agregados:", font=("Helvetica", 14))
        self.product_list_label.grid(row=row, columnspan=3)

        row += 1
        self.product_listbox = tk.Listbox(self.root, width=50)
        self.product_listbox.grid(row=row, columnspan=3, padx=10, pady=10)

    def add_product(self):
        section = self.section_var.get()
        product_name = simpledialog.askstring("Input", "Ingrese el nombre del producto:")
        if not product_name:
            messagebox.showerror("Error", "Nombre del producto no válido.")
            return

        price = simpledialog.askfloat("Input", f"Ingrese el precio del producto: '{product_name}'")
        if price is None or price < 0:
            messagebox.showerror("Error", "Precio no válido.")
            return

        self.sections[section].append((product_name, price))
        messagebox.showinfo("Info", f"Producto '{product_name}' agregado a la sección '{section}'.")
        self.update_product_list()

    def remove_product(self):
        section = self.section_var.get()
        product_name = simpledialog.askstring("Input", "Ingrese el nombre del producto a eliminar:")
        if not product_name:
            messagebox.showerror("Error", "Nombre del producto no válido.")
            return

        for product in self.sections[section]:
            if product[0] == product_name:
                self.sections[section].remove(product)
                messagebox.showinfo("Info", f"Producto '{product_name}' eliminado de la sección '{section}'.")
                self.update_product_list()
                return
        messagebox.showerror("Error", "Producto no encontrado.")

    def edit_price(self):
        section = self.section_var.get()
        product_name = simpledialog.askstring("Input", "Ingrese el nombre del producto a editar:")
        if not product_name:
            messagebox.showerror("Error", "Nombre del producto no válido.")
            return

        new_price = simpledialog.askfloat("Input", "Ingrese el nuevo precio del producto:")
        if new_price is None or new_price < 0:
            messagebox.showerror("Error", "Precio no válido.")
            return

        for i, product in enumerate(self.sections[section]):
            if product[0] == product_name:
                self.sections[section][i] = (product_name, new_price)
                messagebox.showinfo("Info", f"Precio de '{product_name}' actualizado a {new_price}.")
                self.update_product_list()
                return
        messagebox.showerror("Error", "Producto no encontrado.")

    def update_product_list(self):
        self.product_listbox.delete(0, tk.END)
        for section, products in self.sections.items():
            for product_name, price in products:
                self.product_listbox.insert(tk.END, f"{product_name} - {section} - ${price}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductEditorApp(root)
    root.mainloop()
