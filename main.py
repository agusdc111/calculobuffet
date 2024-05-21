import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen

# Establecer el color de fondo de la ventana
Window.clearcolor = (1, 1, 1, 1)  # Blanco

class MainScreen(Screen):
    total_price = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.sections = self.load_products()
        self.quantities = {}
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # ScrollView para secciones
        scroll_view = ScrollView()
        self.sections_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.sections_layout.bind(minimum_height=self.sections_layout.setter('height'))
        scroll_view.add_widget(self.sections_layout)

        root.add_widget(scroll_view)

        # Contenedor para los botones
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=10)

        # Botón para limpiar el carrito
        clear_button = Button(
            text="Limpiar carrito",
            background_color=(0.2, 0.6, 0.86, 1),  # Color azul
            color=(1, 1, 1, 1),  # Texto blanco
            font_size='18sp'
        )
        clear_button.bind(on_press=self.clear_cart)
        button_layout.add_widget(clear_button)

        # Botón para ver el total
        total_button = Button(
            text="Ver total",
            background_color=(0.2, 0.6, 0.86, 1),  # Color azul
            color=(1, 1, 1, 1),  # Texto blanco
            font_size='18sp'
        )
        total_button.bind(on_press=self.show_total)
        button_layout.add_widget(total_button)

        root.add_widget(button_layout)

        # Etiqueta para mostrar el precio total
        self.total_label = Label(
            text="Total: $0.0",
            size_hint_y=None,
            height=dp(50),  # Ajusta la altura en densidad independiente de píxeles (dp)
            color=(0, 0, 0, 1),  # Texto negro
            font_size='18sp'
        )
        root.add_widget(self.total_label)

        self.add_widget(root)

        # Crear widgets de productos
        self.create_product_widgets()
        self.update_total()

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
                height=dp(50),  # Ajusta la altura en densidad independiente de píxeles (dp)
                color=(0.2, 0.6, 0.86, 1),  # Color azul
                font_size='20sp',
                bold=True
            ))
            for product_name, price in section_products:
                product_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(50))
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
                # Botón "-"
                minus_button = Button(
                    text="-",
                    size_hint_x=0.15,
                    width=dp(50),  # Ajusta el ancho en densidad independiente de píxeles (dp)
                    background_color=(0.8, 0.2, 0.2, 1),  # Color rojo
                    color=(1, 1, 1, 1),  # Texto blanco
                    font_size='16sp',
                    on_press=lambda x, name=product_name: self.update_quantity(name, -1)
                )
                product_layout.add_widget(minus_button)

                # Etiqueta de cantidad
                quantity_label = Label(
                    text="0",
                    size_hint_x=0.05,
                    color=(0, 0, 0, 1),  # Texto negro
                    font_size='16sp'
                )
                self.quantities[product_name] = quantity_label
                product_layout.add_widget(quantity_label)

                # Botón "+"
                plus_button = Button(
                    text="+",
                    size_hint_x=0.15,
                    width=dp(50),  # Ajusta el ancho en densidad independiente de píxeles (dp)
                    background_color=(0.2, 0.8, 0.2, 1),  # Color verde
                    color=(1, 1, 1, 1),  # Texto blanco
                    font_size='16sp',
                    on_press=lambda x, name=product_name: self.update_quantity(name, 1)
                )
                product_layout.add_widget(plus_button)

                self.sections_layout.add_widget(product_layout)

    def update_quantity(self, product_name, change):
        new_quantity = max(int(self.quantities[product_name].text) + change, 0)
        self.quantities[product_name].text = str(new_quantity)
        self.update_total()

    def update_total(self):
        total = sum(int(quantity.text) * price for section in self.sections.values() for product, price in section for quantity in [self.quantities[product]])
        self.total_price = total
        self.total_label.text = f"Total: ${total:.2f}"

    def clear_cart(self, instance):
        for quantity_label in self.quantities.values():
            quantity_label.text = '0'
        self.update_total()

    def show_total(self, instance):
        app = App.get_running_app()
        app.root.current = 'total_screen'
        app.root.get_screen('total_screen').update_total_info(self.sections, self.quantities)


class TotalScreen(Screen):
    def __init__(self, **kwargs):
        super(TotalScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Agregar imagen en la parte superior
        image = Image(source="data/banner.webp", allow_stretch=True, keep_ratio=False, size_hint_y=None, height=dp(100))
        layout.add_widget(image)
        
        # ScrollView para el contenido de los productos
        scroll_view = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        scroll_view.add_widget(self.content_layout)

        layout.add_widget(scroll_view)

        # Botón para regresar a la pantalla principal
        back_button = Button(
            text="Regresar",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.86, 1),  # Color azul
            color=(1, 1, 1, 1),  # Texto blanco
            font_size='18sp'
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def update_total_info(self, sections, quantities):
        self.content_layout.clear_widgets()
        for section_name, section_products in sections.items():
            # Verificar si hay productos seleccionados en la sección
            if any(int(quantities[product_name].text) > 0 for product_name, price in section_products):
                self.content_layout.add_widget(Label(
                    text=section_name,
                    size_hint_y=None,
                    height=dp(50),
                    color=(0.2, 0.6, 0.86, 1),  # Color azul
                    font_size='20sp',
                    bold=True
                ))
                for product_name, price in section_products:
                    quantity = int(quantities[product_name].text)
                    if quantity > 0:
                        product_info = f"{product_name} x {quantity} = ${price * quantity:.2f}"
                        self.content_layout.add_widget(Label(
                            text=product_info,
                            size_hint_y=None,
                            height=dp(30),
                            color=(0, 0, 0, 1),  # Texto negro
                            font_size='16sp'
                        ))
        total_price = sum(int(quantities[product].text) * price for section in sections.values() for product, price in section)
        self.content_layout.add_widget(Label(
            text=f"Total: ${total_price:.2f}",
            size_hint_y=None,
            height=dp(50),
            color=(0, 0, 0, 1),  # Texto negro
            font_size='20sp',
            bold=True
        ))

    def go_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'main'


class ShoppingCartApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(TotalScreen(name='total_screen'))
        return sm


if __name__ == "__main__":
    ShoppingCartApp().run()
