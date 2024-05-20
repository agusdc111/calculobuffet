import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty
from kivy.core.window import Window

# Establecer el color de fondo de la ventana
Window.clearcolor = (1, 1, 1, 1)  # Blanco

class ShoppingCartApp(App):
    total_price = NumericProperty(0)

    def build(self):
        self.title = "Shopping Cart"
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.sections = self.load_products()

        # ScrollView para secciones
        scroll_view = ScrollView()
        self.sections_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.sections_layout.bind(minimum_height=self.sections_layout.setter('height'))
        scroll_view.add_widget(self.sections_layout)

        root.add_widget(scroll_view)

        # Botón para limpiar el carrito
        clear_button = Button(
            text="Limpiar carrito",
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.86, 1),  # Color azul
            color=(1, 1, 1, 1),  # Texto blanco
            font_size='18sp'
        )
        clear_button.bind(on_press=self.clear_cart)
        root.add_widget(clear_button)

        # Etiqueta para mostrar el precio total
        self.total_label = Label(
            text="Total: $0",
            size_hint_y=None,
            height=50,
            color=(0, 0, 0, 1),  # Texto negro
            font_size='18sp'
        )
        root.add_widget(self.total_label)

        # Inicializar el diccionario de cantidades
        self.quantities = {}

        # Crear widgets de productos
        self.create_product_widgets()

        self.update_total()
        return root

    def load_products(self):
        try:
            with open('products.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"Bebidas": [], "Dulce": [], "Salado": []}

    def create_product_widgets(self):
        for section_name, section_products in self.sections.items():
            self.sections_layout.add_widget(Label(
                text=section_name,
                size_hint_y=None,
                height=50,
                color=(0.2, 0.6, 0.86, 1),  # Color azul
                font_size='20sp',
                bold=True
            ))
            for product_name, price in section_products:
                product_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
                product_layout.add_widget(Label(
                    text=product_name,
                    size_hint_x=0.7,
                    color=(0, 0, 0, 1),  # Texto negro
                    font_size='16sp'
                ))
                product_layout.add_widget(Label(
                    text=f"${price}",
                    size_hint_x=0.2,
                    color=(0, 0, 0, 1),  # Texto negro
                    font_size='16sp'
                ))
                product_layout.add_widget(Button(
                    text="-",
                    size_hint_x=0.05,
                    background_color=(0.8, 0.2, 0.2, 1),  # Color rojo
                    color=(1, 1, 1, 1),  # Texto blanco
                    font_size='16sp',
                    on_press=lambda x, name=product_name: self.update_quantity(name, -1)
                ))
                quantity_label = Label(
                    text="0",
                    size_hint_x=0.05,
                    color=(0, 0, 0, 1),  # Texto negro
                    font_size='16sp'
                )
                self.quantities[product_name] = quantity_label
                product_layout.add_widget(quantity_label)
                product_layout.add_widget(Button(
                    text="+",
                    size_hint_x=0.05,
                    background_color=(0.2, 0.8, 0.2, 1),  # Color verde
                    color=(1, 1, 1, 1),  # Texto blanco
                    font_size='16sp',
                    on_press=lambda x, name=product_name: self.update_quantity(name, 1)
                ))
                self.sections_layout.add_widget(product_layout)

    def update_quantity(self, product_name, change):
        new_quantity = max(int(self.quantities[product_name].text) + change, 0)
        self.quantities[product_name].text = str(new_quantity)
        self.update_total()

    def update_total(self):
        total = sum(int(quantity.text) * price for section in self.sections.values() for product, price in section for quantity in [self.quantities[product]])
        self.total_price = total
        self.total_label.text = f"Total: ${total}"

    def clear_cart(self, instance):
        for quantity_label in self.quantities.values():
            quantity_label.text = '0'
        self.update_total()


if __name__ == "__main__":
    ShoppingCartApp().run()
