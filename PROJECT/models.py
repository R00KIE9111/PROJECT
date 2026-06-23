class Usuario:
    def __init__(self, rut_usuario, nombre, password, rol="empleado"):
        self.rut_usuario = rut_usuario
        self.nombre = nombre
        self.password = password
        self.rol = rol
    @staticmethod
    def insert_sql():
        return "INSERT INTO Usuario (rut_usuario, nombre, password, rol) VALUES (%s, %s, %s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM Usuario WHERE rut_usuario=%s"

class Equipo:
    def __init__(self, numero_serie, marca, modelo, tipo_equipo):
        self.numero_serie = numero_serie
        self.marca = marca
        self.modelo = modelo
        self.tipo_equipo = tipo_equipo
    @staticmethod
    def insert_sql():
        return "INSERT INTO Equipo (numero_serie, marca, modelo, tipo_equipo) VALUES (%s, %s, %s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM Equipo WHERE numero_serie=%s"

class AsignacionEquipo:
    def __init__(self, rut_usuario, numero_serie, fecha_entrega, fecha_devolucion=None):
        self.rut_usuario = rut_usuario
        self.numero_serie = numero_serie
        self.fecha_entrega = fecha_entrega
        self.fecha_devolucion = fecha_devolucion
    @staticmethod
    def insert_sql():
        return "INSERT INTO AsignacionEquipo (rut_usuario, numero_serie, fecha_entrega, fecha_devolucion) VALUES (%s, %s, %s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM AsignacionEquipo WHERE rut_usuario=%s"

class Sucursal:
    def __init__(self, id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad):
        self.id_sucursal = id_sucursal
        self.correlativo = correlativo
        self.direccion = direccion
        self.telefono = telefono
        self.id_empresa = id_empresa
        self.id_ciudad = id_ciudad
    @staticmethod
    def insert_sql():
        return "INSERT INTO Sucursal (id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad) VALUES (%s, %s, %s, %s, %s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM Sucursal WHERE id_sucursal=%s"

class ServicioTecnico:
    def __init__(self, codigo, nombre_empresa):
        self.codigo = codigo
        self.nombre_empresa = nombre_empresa
    @staticmethod
    def insert_sql():
        return "INSERT INTO ServicioTecnico (codigo, nombre_empresa) VALUES (%s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM ServicioTecnico WHERE codigo=%s"

class HistorialServicio:
    def __init__(self, id_historial, numero_serie, servicio_tecnico, fecha_entrega, fecha_devolucion, motivo_falla, empleado_servicio):
        self.id_historial = id_historial
        self.numero_serie = numero_serie
        self.servicio_tecnico = servicio_tecnico
        self.fecha_entrega = fecha_entrega
        self.fecha_devolucion = fecha_devolucion
        self.motivo_falla = motivo_falla
        self.empleado_servicio = empleado_servicio
    @staticmethod
    def insert_sql():
        return """INSERT INTO HistorialServicio 
                  (id_historial, numero_serie, servicio_tecnico, fecha_entrega, fecha_devolucion, motivo_falla, empleado_servicio) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    @staticmethod
    def select_sql():
        return "SELECT * FROM HistorialServicio WHERE numero_serie=%s"