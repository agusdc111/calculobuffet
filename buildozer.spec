[app]

# Nombre de la aplicación
title = Shopping Cart

# Paquete del aplicativo
package.name = shoppingcart

# Versión del aplicativo
package.version = 1.0

# Código fuente de la aplicación
source.dir = .

# Icono de la aplicación
icon.filename = icon.png

# Versión de Python para usar
requirements.python = 3.7.0

# Dependencias de la aplicación
requirements = kivy, json

# Incluye archivos adicionales
source.include_exts = py, json
source.include_patterns = assets/*, *.py

# Excluye archivos y carpetas
source.exclude_patterns = __pycache__, *.pyc, .git, .hg, .svn

# Permiso para escribir en almacenamiento externo (opcional)
android.permissions = INTERNET

# Otras configuraciones específicas de Android
android.arch = armeabi-v7a
android.entrypoint = indexkivy.py

# Versión de la aplicación
version = 0.1
