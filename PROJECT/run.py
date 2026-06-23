from flask import *
from flask_wtf.csrf import CSRFProtect
from gestion import *

app = Flask(__name__)
app.secret_key = "kt7GphhcBsqf."
csrf = CSRFProtect(app)

@app.route("/")
def index():
    if "usuario" in session:
        return render_template("index.html", usuario=session["usuario"], rol=session.get("rol"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        rut = request.form["rut"]
        password = request.form["password"]
        usuario = validar_login(rut, password)
        if usuario:
            session["usuario"] = rut
            session["rol"] = usuario["rol"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if "usuario" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        rut = request.form["rut"]
        nombre = request.form["nombre"]
        password = request.form["password"]
        rol = request.form.get("rol", "empleado")
        if crear_usuario(rut, nombre, password, rol):
            return redirect(url_for("usuarios"))
        else:
            return render_template("usuarios.html", error="El usuario ya existe", usuarios=listar_usuarios())
    return render_template("usuarios.html", usuarios=listar_usuarios())

@app.route("/usuarios/eliminar/<rut>")
def usuarios_eliminar(rut):
    eliminar_usuario(rut)
    return redirect(url_for("usuarios"))

@app.route("/usuarios/editar/<rut>", methods=["POST"])
def usuarios_editar(rut):
    nombre = request.form["nombre"]
    password = request.form.get("password")
    rol = request.form.get("rol", "empleado")
    editar_usuario(rut, nombre, password, rol)
    return redirect(url_for("usuarios"))

@app.route("/olvide", methods=["GET", "POST"])
def olvide():
    if request.method == "POST":
        rut = request.form["rut"]
        nueva_password = request.form["nueva_password"]
        if resetear_password(rut, nueva_password):
            return redirect(url_for("login"))
        else:
            return render_template("olvide.html", error="Usuario no encontrado")
    return render_template("olvide.html")

@app.route("/equipos", methods=["GET", "POST"])
def equipos():
    if "usuario" not in session or session["rol"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        numero_serie = request.form["numero_serie"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        tipo_equipo = request.form["tipo_equipo"]
        if crear_equipo(numero_serie, marca, modelo, tipo_equipo):
            return redirect(url_for("equipos"))
        else:
            return render_template("equipos.html", error="El equipo ya existe", equipos=listar_equipos())
    return render_template("equipos.html", equipos=listar_equipos())

@app.route("/equipos/eliminar/<numero_serie>")
def equipos_eliminar(numero_serie):
    eliminar_equipo(numero_serie)
    return redirect(url_for("equipos"))

@app.route("/equipos/editar/<numero_serie>", methods=["POST"])
def equipos_editar(numero_serie):
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    tipo_equipo = request.form["tipo_equipo"]
    editar_equipo(numero_serie, marca, modelo, tipo_equipo)
    return redirect(url_for("equipos"))

@app.route("/asignaciones", methods=["GET", "POST"])
def asignaciones():
    if "usuario" not in session or session["rol"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        rut_usuario = request.form["rut_usuario"]
        numero_serie = request.form["numero_serie"]
        fecha_entrega = request.form["fecha_entrega"]
        fecha_devolucion = request.form.get("fecha_devolucion")
        if crear_asignacion(rut_usuario, numero_serie, fecha_entrega, fecha_devolucion):
            return redirect(url_for("asignaciones"))
        else:
            return render_template("asignaciones.html", error="Usuario o equipo no existe", asignaciones=listar_asignaciones())
    return render_template("asignaciones.html", asignaciones=listar_asignaciones())

@app.route("/asignaciones/eliminar/<rut>/<numero_serie>")
def asignaciones_eliminar(rut, numero_serie):
    eliminar_asignacion(rut, numero_serie)
    return redirect(url_for("asignaciones"))

@app.route("/sucursales", methods=["GET", "POST"])
def sucursales():
    if "usuario" not in session or session["rol"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        id_sucursal = request.form["id_sucursal"]
        correlativo = request.form["correlativo"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        id_empresa = request.form["id_empresa"]
        id_ciudad = request.form["id_ciudad"]
        if crear_sucursal(id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad):
            return redirect(url_for("sucursales"))
        else:
            return render_template("sucursales.html", error="La sucursal ya existe", sucursales=listar_sucursales())
    return render_template("sucursales.html", sucursales=listar_sucursales())

@app.route("/sucursales/eliminar/<id_sucursal>")
def sucursales_eliminar(id_sucursal):
    eliminar_sucursal(id_sucursal)
    return redirect(url_for("sucursales"))

@app.route("/sucursales/editar/<id_sucursal>", methods=["POST"])
def sucursales_editar(id_sucursal):
    correlativo = request.form["correlativo"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    id_empresa = request.form["id_empresa"]
    id_ciudad = request.form["id_ciudad"]
    editar_sucursal(id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad)
    return redirect(url_for("sucursales"))

@app.route("/eventos")
def eventos():
    if "usuario" not in session or session["rol"] != "analista":
        return redirect(url_for("login"))
    lista_eventos = listar_eventos()
    return render_template("eventos.html", eventos=lista_eventos)

@app.route("/servicio", methods=["GET", "POST"])
def servicio():
    if "usuario" not in session or session["rol"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        codigo = request.form["codigo"]
        nombre_empresa = request.form["nombre_empresa"]
        if crear_servicio(codigo, nombre_empresa):
            return redirect(url_for("servicio"))
        else:
            return render_template("servicio.html", error="El servicio ya existe", servicios=listar_servicios())
    return render_template("servicio.html", servicios=listar_servicios())

@app.route("/servicio/eliminar/<codigo>")
def servicio_eliminar(codigo):
    eliminar_servicio(codigo)
    return redirect(url_for("servicio"))

@app.route("/servicio/editar/<codigo>", methods=["POST"])
def servicio_editar(codigo):
    nombre_empresa = request.form["nombre_empresa"]
    editar_servicio(codigo, nombre_empresa)
    return redirect(url_for("servicio"))

@app.route("/historial", methods=["GET", "POST"])
def historial():
    if "usuario" not in session or session["rol"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        id_historial = request.form["id_historial"]
        numero_serie = request.form["numero_serie"]
        servicio_tecnico = request.form["servicio_tecnico"]
        fecha_entrega = request.form["fecha_entrega"]
        fecha_devolucion = request.form.get("fecha_devolucion")
        motivo_falla = request.form["motivo_falla"]
        empleado_servicio = request.form["empleado_servicio"]
        if crear_historial(id_historial, numero_serie, servicio_tecnico, fecha_entrega, fecha_devolucion, motivo_falla, empleado_servicio):
            return redirect(url_for("historial"))
        else:
            return render_template("historial.html", error="Equipo no existe", historial=listar_historial())
    return render_template("historial.html", historial=listar_historial())

@app.route("/historial/eliminar/<id_historial>")
def historial_eliminar(id_historial):
    eliminar_historial(id_historial)
    return redirect(url_for("historial"))

@app.route("/mis_equipos")
def mis_equipos_view():
    if "usuario" not in session or session["rol"] != "cliente":
        return redirect(url_for("login"))
    lista = mis_equipos(session["usuario"])
    return render_template("mis_equipos.html", equipos=lista)

@app.route("/mis_asignaciones")
def mis_asignaciones_view():
    if "usuario" not in session or session["rol"] != "cliente":
        return redirect(url_for("login"))
    lista = mis_asignaciones(session["usuario"])
    return render_template("mis_asignaciones.html", asignaciones=lista)

@app.route("/mis_historiales")
def mis_historiales_view():
    if "usuario" not in session or session["rol"] != "cliente":
        return redirect(url_for("login"))
    lista = mis_historiales(session["usuario"])
    return render_template("mis_historiales.html", historial=lista)

if __name__ == "__main__":
    app.run(debug=True)