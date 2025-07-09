# web_login_flask.py
from flask import Flask, request, render_template_string
import sqlite3
import hashlib

# Crear base de datos y tabla si no existen
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            nombre TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Agregar usuario
def agregar_usuario(nombre, contraseña):
    hash_pass = hashlib.sha256(contraseña.encode()).hexdigest()
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, hash_pass))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ya existe
    conn.close()

# Verificar credenciales
def validar_usuario(nombre, contraseña):
    hash_pass = hashlib.sha256(contraseña.encode()).hexdigest()
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre = ? AND password_hash = ?", (nombre, hash_pass))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# Inicializar base de datos y agregar integrantes (ejemplo)
init_db()
agregar_usuario("diego", "clave123")
agregar_usuario("juan", "clave456")
agregar_usuario("Johan", "clave789")
agregar_usuario("Lucas", "clave347")

# Aplicación Flask
app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<title>Login de Examen</title>
<h2>Ingreso de Usuarios</h2>
<form method="POST">
  Nombre: <input type="text" name="nombre"><br>
  Contraseña: <input type="password" name="password"><br>
  <input type="submit" value="Ingresar">
</form>
<p>{{ mensaje }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        nombre = request.form["nombre"]
        password = request.form["password"]
        if validar_usuario(nombre, password):
            mensaje = "Acceso concedido"
        else:
            mensaje = "Credenciales inválidas"
    return render_template_string(HTML_FORM, mensaje=mensaje)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800)
