import pymysql
from werkzeug.security import generate_password_hash

def populate():
    db = pymysql.connect(
        host='eva3-aws-azure-db.c7saowikmas3.us-east-1.rds.amazonaws.com',
        user='admin',
        password='kt7GphhcBsqf.',
        database='project'
    )
    cursor = db.cursor()

    queries = [
        # Limpiar
        "SET FOREIGN_KEY_CHECKS = 0;",
        "TRUNCATE TABLE HistorialServicio;",
        "TRUNCATE TABLE AsignacionEquipo;",
        "TRUNCATE TABLE Equipo;",
        "TRUNCATE TABLE ServicioTecnico;",
        "TRUNCATE TABLE Usuario;",
        "TRUNCATE TABLE Sucursal;",
        "TRUNCATE TABLE Area;",
        "TRUNCATE TABLE Empresa;",
        "TRUNCATE TABLE Ciudad;",
        "TRUNCATE TABLE Pais;",
        "TRUNCATE TABLE TipoEquipo;",
        "SET FOREIGN_KEY_CHECKS = 1;",

        # Insertar Pais
        "INSERT INTO Pais (codigo, nombre) VALUES ('CL', 'Chile');",
        
        # Insertar Ciudades
        "INSERT INTO Ciudad (id_ciudad, nombre, id_pais) VALUES (1, 'Antofagasta', 'CL');",
        "INSERT INTO Ciudad (id_ciudad, nombre, id_pais) VALUES (2, 'Calama', 'CL');",
        
        # Insertar Empresas
        "INSERT INTO Empresa (id_empresa, nombre) VALUES (1, 'Metso Minerals');",
        "INSERT INTO Empresa (id_empresa, nombre) VALUES (2, 'BHP Billiton');",
        
        # Insertar Sucursales
        "INSERT INTO Sucursal (id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad) VALUES ('S1', 1, 'General Velázquez #452', '123', 1, 1);",
        "INSERT INTO Sucursal (id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad) VALUES ('S2', 2, 'Otra Direccion', '123', 1, 2);",
        "INSERT INTO Sucursal (id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad) VALUES ('S3', 3, 'BHP Calama', '123', 2, 2);",
        "INSERT INTO Sucursal (id_sucursal, correlativo, direccion, telefono, id_empresa, id_ciudad) VALUES ('S4', 4, 'BHP Antofagasta', '123', 2, 1);",
        
        # Insertar Areas
        "INSERT INTO Area (codigo, nombre, id_empresa) VALUES ('A1', 'Recursos humanos', 1);",
        "INSERT INTO Area (codigo, nombre, id_empresa) VALUES ('A2', 'Prevención de riesgos', 1);",
        "INSERT INTO Area (codigo, nombre, id_empresa) VALUES ('A3', 'Informática', 2);",
        
        # Insertar TipoEquipo
        "INSERT INTO TipoEquipo (codigo, nombre) VALUES ('TE1', 'notebook');",
        "INSERT INTO TipoEquipo (codigo, nombre) VALUES ('TE2', 'Celular');",
        
        # Insertar ServicioTecnico
        "INSERT INTO ServicioTecnico (codigo, nombre_empresa) VALUES ('ST1', 'Sonda');",
    ]

    for q in queries:
        cursor.execute(q)

    # Usuarios
    pw = generate_password_hash('123456')
    usuarios = [
        ("1-1", "Tony Stark", pw, "empleado", "tony@stark.com", "A1", "S1", 30),
        ("2-2", "Admin", pw, "admin", "admin@test.com", "A3", "S3", 40),
        ("3-3", "Old Guy", pw, "empleado", "old@bhp.com", "A3", "S3", 55), # Para query usuarios > 50 BHP
        ("4-4", "Analista", pw, "analista", "analyst@test.com", "A1", "S1", 25) # Rol analista
    ]
    for u in usuarios:
        cursor.execute("INSERT INTO Usuario (rut_usuario, nombre, password, rol, email, id_area, id_sucursal, edad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", u)

    # Equipos
    equipos = [
        ("EQ1", "Dell", "XPS", "notebook", "TE1"),
        ("EQ2", "Samsung", "S3", "Celular", "TE2"),
        ("EQ3", "Apple", "MacBook", "notebook", "TE1")
    ]
    for e in equipos:
        cursor.execute("INSERT INTO Equipo (numero_serie, marca, modelo, tipo_equipo, codigo_tipo_equipo) VALUES (%s, %s, %s, %s, %s)", e)

    # Asignaciones
    asignaciones = [
        ("1-1", "EQ1", "2023-01-01"), # Tony con notebook en Chile
        ("3-3", "EQ2", "2023-02-01"), # Celular Samsung S3 en Calama
    ]
    for a in asignaciones:
        cursor.execute("INSERT INTO AsignacionEquipo (rut_usuario, numero_serie, fecha_entrega) VALUES (%s, %s, %s)", a)

    # Historial Servicio
    historial = [
        ("H1", "EQ1", "ST1", "2023-03-01", "2023-03-10", "Falla disco duro", "Juan Perez")
    ]
    for h in historial:
        cursor.execute("INSERT INTO HistorialServicio (id_historial, numero_serie, servicio_tecnico, fecha_entrega, fecha_devolucion, motivo_falla, empleado_servicio) VALUES (%s, %s, %s, %s, %s, %s, %s)", h)

    db.commit()
    db.close()
    print("Base de datos poblada exitosamente.")

if __name__ == "__main__":
    populate()
