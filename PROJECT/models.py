class Pais:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
    @staticmethod
    def insert_sql():
        return "INSERT INTO Pais (codigo, nombre) VALUES (%s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM Pais WHERE codigo=%s"

class TipoEquipo:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
    @staticmethod
    def insert_sql():
        return "INSERT INTO TipoEquipo (codigo, nombre) VALUES (%s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM TipoEquipo WHERE codigo=%s"

class Empresa:
    def __init__(self, id_empresa, nombre):
        self.id_empresa = id_empresa
        self.nombre = nombre
    @staticmethod
    def insert_sql():
        return "INSERT INTO Empresa (id_empresa, nombre) VALUES (%s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM Empresa WHERE id_empresa=%s"

class Ciudad:
    def __init__(self, id_ciudad, nombre, id_pais):
        self.id_ciudad = id_ciudad
        self.nombre = nombre
        self.id_pais = id_pais
    @staticmethod
    def insert_sql():
        return "INSERT INTO Ciudad (id_ciudad, nombre, id_pais) VALUES (%s, %s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM Ciudad WHERE id_ciudad=%s"

class Area:
    def __init__(self, codigo, nombre, id_empresa, id_gerente):
        self.codigo = codigo
        self.nombre = nombre
        self.id_empresa = id_empresa
        self.id_gerente = id_gerente
    @staticmethod
    def insert_sql():
        return "INSERT INTO Area (codigo, nombre, id_empresa, id_gerente) VALUES (%s, %s, %s, %s)"
    @staticmethod
    def select_sql():
        return "SELECT * FROM Area WHERE codigo=%s"

class Usuario:
    def __init__(self, rut_usuario, nombre, password, rol="empleado", 
                 apellido_paterno=None, apellido_materno=None, fecha_nacimiento=None,
                 edad=None, direccion=None, anexo=None, email=None, celular=None, 
                 id_area=None, oficina=None):
        self.rut_usuario = rut_usuario
        self.nombre = nombre
        self.password = password
        self.rol = rol
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = edad
        self.direccion = direccion
        self.anexo = anexo
        self.email = email
        self.celular = celular
        self.id_area = id_area
        self.oficina = oficina
    @staticmethod
    def insert_sql():
        return """INSERT INTO Usuario (rut_usuario, nombre, password, rol, apellido_paterno, apellido_materno, fecha_nacimiento, edad, direccion, anexo, email, celular, id_area, oficina) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    @staticmethod
    def select_sql():
        return "SELECT * FROM Usuario WHERE rut_usuario=%s"

class Equipo:
    def __init__(self, numero_serie, marca, modelo, tipo_equipo, es_reemplazo=False, codigo_tipo_equipo=None):
        self.numero_serie = numero_serie
        self.marca = marca
        self.modelo = modelo
        self.tipo_equipo = tipo_equipo # Legacy
        self.es_reemplazo = es_reemplazo
        self.codigo_tipo_equipo = codigo_tipo_equipo
    @staticmethod
    def insert_sql():
        return "INSERT INTO Equipo (numero_serie, marca, modelo, tipo_equipo, es_reemplazo, codigo_tipo_equipo) VALUES (%s, %s, %s, %s, %s, %s)"
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