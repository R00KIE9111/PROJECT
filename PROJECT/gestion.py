from database import *
from models import *
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

def validar_login(rut, password):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(Usuario.select_sql(), (rut,))
    usuario = cursor.fetchone()
    db.close()
    if usuario and check_password_hash(usuario["password"], password):
        registrar_evento(rut, "login", "Inicio de sesión exitoso")
        return usuario
    return None

def resetear_password(rut, nueva_password):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(Usuario.select_sql(), (rut,))
    usuario = cursor.fetchone()
    if not usuario:
        db.close()
        return False
    hashed_pw = generate_password_hash(nueva_password)
    cursor.execute("UPDATE Usuario SET password=%s WHERE rut_usuario=%s", (hashed_pw, rut))
    db.commit()
    db.close()
    registrar_evento(rut, "reset_password", "Contraseña restablecida")
    return True

def crear_usuario(rut, nombre, password, rol="empleado"):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(Usuario.select_sql(), (rut,))
    existente = cursor.fetchone()
    if existente:
        db.close()
        return False
    hashed_pw = generate_password_hash(password)
    usuario = Usuario(rut, nombre, hashed_pw, rol)
    cursor.execute("INSERT INTO Usuario (rut_usuario, nombre, password, rol) VALUES (%s, %s, %s, %s)", 
                   (usuario.rut_usuario, usuario.nombre, usuario.password, usuario.rol))
    db.commit()
    db.close()
    registrar_evento(rut, "crear_usuario", f"Usuario {nombre} creado")
    return True

def listar_usuarios():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT rut_usuario, nombre, rol FROM Usuario")
    lista = cursor.fetchall()
    db.close()
    return lista

def eliminar_usuario(rut):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM Usuario WHERE rut_usuario=%s", (rut,))
    db.commit()
    db.close()
    registrar_evento(rut, "eliminar_usuario", f"Usuario {rut} eliminado")

def editar_usuario(rut, nombre=None, password=None, rol=None):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if password:
        password = generate_password_hash(password)
        cursor.execute("UPDATE Usuario SET nombre=%s, password=%s, rol=%s WHERE rut_usuario=%s",
                       (nombre, password, rol, rut))
    else:
        cursor.execute("UPDATE Usuario SET nombre=%s, rol=%s WHERE rut_usuario=%s",
                       (nombre, rol, rut))
    db.commit()
    db.close()
    registrar_evento(rut, "editar_usuario", f"Usuario {rut} editado")

def crear_equipo(numero_serie, marca, modelo, tipo_equipo):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(Equipo.select_sql(), (numero_serie,))
    existente = cursor.fetchone()
    if existente:
        db.close()
        return False
    equipo = Equipo(numero_serie, marca, modelo, tipo_equipo)
    cursor.execute("INSERT INTO Equipo (numero_serie, marca, modelo, tipo_equipo) VALUES (%s, %s, %s, %s)", 
                   (equipo.numero_serie, equipo.marca, equipo.modelo, equipo.tipo_equipo))
    db.commit()
    db.close()
    registrar_evento(numero_serie, "crear_equipo", f"Equipo {marca} {modelo} creado")
    return True

def listar_equipos():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT numero_serie, marca, modelo, tipo_equipo FROM Equipo")
    lista = cursor.fetchall()
    db.close()
    return lista

def eliminar_equipo(numero_serie):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM Equipo WHERE numero_serie=%s", (numero_serie,))
    db.commit()
    db.close()
    registrar_evento(numero_serie, "eliminar_equipo", f"Equipo {numero_serie} eliminado")

def editar_equipo(numero_serie, marca, modelo, tipo_equipo):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("UPDATE Equipo SET marca=%s, modelo=%s, tipo_equipo=%s WHERE numero_serie=%s",
                   (marca, modelo, tipo_equipo, numero_serie))
    db.commit()
    db.close()
    registrar_evento(numero_serie, "editar_equipo", f"Equipo {numero_serie} editado")

def crear_asignacion(rut_usuario, numero_serie, fecha_entrega, fecha_devolucion=None):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(Usuario.select_sql(), (rut_usuario,))
    usuario = cursor.fetchone()
    if not usuario:
        db.close()
        return False
    cursor.execute(Equipo.select_sql(), (numero_serie,))
    equipo = cursor.fetchone()
    if not equipo:
        db.close()
        return False

    asignacion = AsignacionEquipo(rut_usuario, numero_serie, fecha_entrega, fecha_devolucion)
    cursor.execute(AsignacionEquipo.insert_sql(),
                   (asignacion.rut_usuario, asignacion.numero_serie,
                    asignacion.fecha_entrega, asignacion.fecha_devolucion))
    db.commit()
    db.close()
    registrar_evento(rut_usuario, "crear_asignacion", f"Equipo {numero_serie} asignado")
    return True

def listar_asignaciones():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT a.rut_usuario, u.nombre, e.marca, e.modelo, a.fecha_entrega, a.fecha_devolucion
        FROM AsignacionEquipo a
        JOIN Usuario u ON a.rut_usuario = u.rut_usuario
        JOIN Equipo e ON a.numero_serie = e.numero_serie
    """)
    lista = cursor.fetchall()
    db.close()
    return lista

def eliminar_asignacion(rut_usuario, numero_serie):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM AsignacionEquipo WHERE rut_usuario=%s AND numero_serie=%s", (rut_usuario, numero_serie))
    db.commit()
    db.close()
    registrar_evento(rut_usuario, "eliminar_asignacion", f"Equipo {numero_serie} devuelto")

def crear_sucursal(id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(Sucursal.select_sql(), (id_sucursal,))
    existente = cursor.fetchone()
    if existente:
        db.close()
        return False
    sucursal = Sucursal(id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad)
    cursor.execute(Sucursal.insert_sql(),
                   (sucursal.id_sucursal, sucursal.correlativo, sucursal.direccion,
                    sucursal.telefono, sucursal.id_empresa, sucursal.id_ciudad))
    db.commit()
    db.close()
    registrar_evento(id_sucursal, "crear_sucursal", f"Sucursal {direccion} creada")
    return True

def listar_sucursales():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT s.id_sucursal, s.correlativo, s.direccion, s.telefono,
               e.nombre AS empresa, c.nombre AS ciudad
        FROM Sucursal s
        LEFT JOIN Empresa e ON s.id_empresa = e.id_empresa
        LEFT JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
    """)
    lista = cursor.fetchall()
    db.close()
    return lista

def eliminar_sucursal(id_sucursal):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM Sucursal WHERE id_sucursal=%s", (id_sucursal,))
    db.commit()
    db.close()
    registrar_evento(id_sucursal, "eliminar_sucursal", f"Sucursal {id_sucursal} eliminada")

def editar_sucursal(id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""UPDATE Sucursal 
                      SET correlativo=%s, direccion=%s, telefono=%s, id_empresa=%s, id_ciudad=%s 
                      WHERE id_sucursal=%s""",
                   (correlativo, direccion, telefono, id_empresa, id_ciudad, id_sucursal))
    db.commit()
    db.close()
    registrar_evento(id_sucursal, "editar_sucursal", f"Sucursal {id_sucursal} editada")

def crear_servicio(codigo, nombre_empresa):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(ServicioTecnico.select_sql(), (codigo,))
    existente = cursor.fetchone()
    if existente:
        db.close()
        return False
    servicio = ServicioTecnico(codigo, nombre_empresa)
    cursor.execute(ServicioTecnico.insert_sql(), (servicio.codigo, servicio.nombre_empresa))
    db.commit()
    db.close()
    registrar_evento(codigo, "crear_servicio", f"Servicio técnico {nombre_empresa} creado")
    return True

def listar_servicios():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT codigo, nombre_empresa FROM ServicioTecnico")
    lista = cursor.fetchall()
    db.close()
    return lista

def eliminar_servicio(codigo):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM ServicioTecnico WHERE codigo=%s", (codigo,))
    db.commit()
    db.close()
    registrar_evento(codigo, "eliminar_servicio", f"Servicio técnico {codigo} eliminado")

def editar_servicio(codigo, nombre_empresa):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("UPDATE ServicioTecnico SET nombre_empresa=%s WHERE codigo=%s", (nombre_empresa, codigo))
    db.commit()
    db.close()
    registrar_evento(codigo, "editar_servicio", f"Servicio técnico {codigo} editado")

def crear_historial(id_historial, numero_serie, servicio_tecnico, fecha_entrega, fecha_devolucion, motivo_falla, empleado_servicio):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(Equipo.select_sql(), (numero_serie,))
    equipo = cursor.fetchone()
    if not equipo:
        db.close()
        return False
    historial = HistorialServicio(id_historial, numero_serie, servicio_tecnico, fecha_entrega, fecha_devolucion, motivo_falla, empleado_servicio)
    cursor.execute(HistorialServicio.insert_sql(),
                   (historial.id_historial, historial.numero_serie, historial.servicio_tecnico,
                    historial.fecha_entrega, historial.fecha_devolucion, historial.motivo_falla, historial.empleado_servicio))
    db.commit()
    db.close()
    registrar_evento(numero_serie, "crear_historial", f"Equipo {numero_serie} enviado a servicio técnico")
    return True

def listar_historial():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT h.id_historial, e.marca, e.modelo, s.nombre_empresa,
               h.fecha_entrega, h.fecha_devolucion, h.motivo_falla, h.empleado_servicio
        FROM HistorialServicio h
        JOIN Equipo e ON h.numero_serie = e.numero_serie
        JOIN ServicioTecnico s ON h.servicio_tecnico = s.codigo
    """)
    lista = cursor.fetchall()
    db.close()
    return lista

def eliminar_historial(id_historial):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM HistorialServicio WHERE id_historial=%s", (id_historial,))
    db.commit()
    db.close()
    registrar_evento(id_historial, "eliminar_historial", f"Historial {id_historial} eliminado")

def mis_equipos(rut_usuario):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT e.numero_serie, e.marca, e.modelo, e.tipo_equipo
        FROM Equipo e
        JOIN AsignacionEquipo a ON e.numero_serie = a.numero_serie
        WHERE a.rut_usuario=%s
    """, (rut_usuario,))
    lista = cursor.fetchall()
    db.close()
    return lista

def mis_asignaciones(rut_usuario):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT a.numero_serie, e.marca, e.modelo, a.fecha_entrega, a.fecha_devolucion
        FROM AsignacionEquipo a
        JOIN Equipo e ON a.numero_serie = e.numero_serie
        WHERE a.rut_usuario=%s
    """, (rut_usuario,))
    lista = cursor.fetchall()
    db.close()
    return lista

def mis_historiales(rut_usuario):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT h.id_historial, e.marca, e.modelo, s.nombre_empresa AS servicio_tecnico,
               h.fecha_entrega, h.fecha_devolucion, h.motivo_falla, h.empleado_servicio
        FROM HistorialServicio h
        JOIN AsignacionEquipo a ON h.numero_serie = a.numero_serie
        JOIN Equipo e ON h.numero_serie = e.numero_serie
        JOIN ServicioTecnico s ON h.servicio_tecnico = s.codigo
        WHERE a.rut_usuario=%s
    """, (rut_usuario,))
    lista = cursor.fetchall()
    db.close()
    return lista

def listar_eventos():
    items = container.read_all_items()
    eventos = []
    for item in items:
        eventos.append({
            "usuario": item.get("usuario"),
            "accion": item.get("accion"),
            "detalle": item.get("detalle"),
            "resultado": item.get("resultado")
        })
    return eventos

# --- REQUERIMIENTOS DEL SISTEMA (CONSULTAS) ---

def req1_notebooks_chile():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT DISTINCT e.marca, e.modelo 
        FROM Equipo e
        LEFT JOIN TipoEquipo te ON e.codigo_tipo_equipo = te.codigo
        JOIN AsignacionEquipo ae ON e.numero_serie = ae.numero_serie
        JOIN Usuario u ON ae.rut_usuario = u.rut_usuario
        JOIN Sucursal s ON u.id_sucursal = s.id_sucursal
        JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
        JOIN Pais p ON c.id_pais = p.codigo
        WHERE (e.tipo_equipo LIKE '%notebook%' OR te.nombre LIKE '%notebook%')
          AND p.nombre = 'Chile'
    """)
    lista = cursor.fetchall()
    db.close()
    return lista

def req2_empleados_metso_antofagasta():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT u.rut_usuario, u.nombre, u.apellido_paterno, u.apellido_materno
        FROM Usuario u
        JOIN Area ar ON u.id_area = ar.codigo
        JOIN Empresa emp ON ar.id_empresa = emp.id_empresa
        JOIN Sucursal s ON u.id_sucursal = s.id_sucursal
        JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
        JOIN Pais p ON c.id_pais = p.codigo
        WHERE (ar.nombre = 'Recursos humanos' OR ar.nombre = 'Prevención de riesgos')
          AND emp.nombre = 'Metso Minerals'
          AND p.nombre = 'Chile'
          AND c.nombre = 'Antofagasta'
          AND s.direccion LIKE '%General Velázquez #452%'
    """)
    lista = cursor.fetchall()
    db.close()
    return lista

def req3_celular_samsung_calama():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT DISTINCT u.rut_usuario, u.nombre, u.apellido_paterno
        FROM Usuario u
        JOIN AsignacionEquipo ae ON u.rut_usuario = ae.rut_usuario
        JOIN Equipo e ON ae.numero_serie = e.numero_serie
        JOIN Sucursal s ON u.id_sucursal = s.id_sucursal
        JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
        WHERE (e.tipo_equipo LIKE '%Celular%' OR e.codigo_tipo_equipo IN (SELECT codigo FROM TipoEquipo WHERE nombre LIKE '%Celular%'))
          AND e.marca = 'Samsung'
          AND e.modelo = 'S3'
          AND c.nombre = 'Calama'
    """)
    lista = cursor.fetchall()
    db.close()
    return lista

def req4_equipos_tony_stark():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT e.numero_serie, e.marca, e.modelo, e.tipo_equipo
        FROM Equipo e
        JOIN AsignacionEquipo ae ON e.numero_serie = ae.numero_serie
        JOIN Usuario u ON ae.rut_usuario = u.rut_usuario
        WHERE u.nombre = 'Tony Stark'
    """)
    lista = cursor.fetchall()
    db.close()
    return lista

def req5_cantidad_sucursales_metso_antofagasta():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT COUNT(s.id_sucursal) as total
        FROM Sucursal s
        JOIN Empresa emp ON s.id_empresa = emp.id_empresa
        JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
        WHERE emp.nombre = 'Metso Minerals' AND c.nombre = 'Antofagasta'
    """)
    resultado = cursor.fetchone()
    db.close()
    return resultado["total"] if resultado else 0

def req6_usuarios_mayores_50_bhp_informatica():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT COUNT(u.rut_usuario) as total
        FROM Usuario u
        JOIN Area ar ON u.id_area = ar.codigo
        JOIN Empresa emp ON ar.id_empresa = emp.id_empresa
        WHERE u.edad > 50 
          AND ar.nombre = 'Informática'
          AND emp.nombre = 'BHP Billiton'
    """)
    resultado = cursor.fetchone()
    db.close()
    return resultado["total"] if resultado else 0

def req7_empleados_bhp_ciudad(nombre_ciudad):
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT u.rut_usuario, u.nombre, u.apellido_paterno
        FROM Usuario u
        JOIN Sucursal s ON u.id_sucursal = s.id_sucursal
        JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
        JOIN Empresa emp ON s.id_empresa = emp.id_empresa
        WHERE emp.nombre = 'BHP Billiton' AND c.nombre = %s
    """, (nombre_ciudad,))
    lista = cursor.fetchall()
    db.close()
    return lista

def req8_equipos_servicio_metso_antofagasta():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT e.tipo_equipo, e.modelo, e.marca,
               h.fecha_entrega, h.fecha_devolucion as fecha_devolucion_estimada, h.motivo_falla, h.empleado_servicio
        FROM HistorialServicio h
        JOIN Equipo e ON h.numero_serie = e.numero_serie
        JOIN AsignacionEquipo ae ON e.numero_serie = ae.numero_serie
        JOIN Usuario u ON ae.rut_usuario = u.rut_usuario
        JOIN Sucursal s ON u.id_sucursal = s.id_sucursal
        JOIN Empresa emp ON s.id_empresa = emp.id_empresa
        JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
        WHERE emp.nombre = 'Metso Minerals' AND c.nombre = 'Antofagasta'
    """)
    lista = cursor.fetchall()
    db.close()
    return lista

def req9_equipos_sonda_metso_antofagasta():
    db = conexion()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT e.numero_serie, e.marca, e.modelo, e.tipo_equipo
        FROM HistorialServicio h
        JOIN ServicioTecnico st ON h.servicio_tecnico = st.codigo
        JOIN Equipo e ON h.numero_serie = e.numero_serie
        JOIN AsignacionEquipo ae ON e.numero_serie = ae.numero_serie
        JOIN Usuario u ON ae.rut_usuario = u.rut_usuario
        JOIN Sucursal s ON u.id_sucursal = s.id_sucursal
        JOIN Empresa emp ON s.id_empresa = emp.id_empresa
        JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
        WHERE st.nombre_empresa = 'Sonda'
          AND emp.nombre = 'Metso Minerals'
          AND c.nombre = 'Antofagasta'
    """)
    lista = cursor.fetchall()
    db.close()
    return lista
