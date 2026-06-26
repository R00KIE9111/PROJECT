import pymysql
import random
from faker import Faker
from werkzeug.security import generate_password_hash

def populate_masivo(num_records=100):
    fake = Faker('es_CL')
    
    db = pymysql.connect(
        host='eva3-aws-azure-db.c7saowikmas3.us-east-1.rds.amazonaws.com',
        user='admin',
        password='kt7GphhcBsqf.',
        database='project'
    )
    cursor = db.cursor()

    pw = generate_password_hash('123456')
    
    # Obtener áreas, sucursales y tipos de equipo existentes para asignar aleatoriamente
    cursor.execute("SELECT codigo FROM Area")
    areas = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id_sucursal FROM Sucursal")
    sucursales = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT codigo FROM TipoEquipo")
    tipos = [row[0] for row in cursor.fetchall()]

    if not areas or not sucursales or not tipos:
        print("Error: Debes ejecutar primero el poblamiento base (las tablas catálogo están vacías).")
        return

    print(f"Generando {num_records} usuarios...")
    rut_generados = []
    for _ in range(num_records):
        rut = fake.unique.numerify(text='########-#')
        rut_generados.append(rut)
        nombre = fake.name()
        email = fake.unique.email()
        edad = random.randint(20, 65)
        rol = random.choice(['empleado', 'empleado', 'empleado', 'admin']) # Mayoría empleados
        area = random.choice(areas)
        sucursal = random.choice(sucursales)
        
        cursor.execute("""
            INSERT INTO Usuario (rut_usuario, nombre, password, rol, email, id_area, id_sucursal, edad) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (rut, nombre, pw, rol, email, area, sucursal, edad))

    print(f"Generando {num_records} equipos...")
    equipos_generados = []
    marcas = ['HP', 'Lenovo', 'Dell', 'Apple', 'Samsung', 'Motorola', 'Asus', 'Acer']
    for _ in range(num_records):
        n_serie = fake.unique.bothify(text='SN-######-??')
        equipos_generados.append(n_serie)
        marca = random.choice(marcas)
        modelo = fake.word().capitalize() + " " + str(random.randint(10, 99))
        tipo = random.choice(tipos)
        tipo_nombre = 'Notebook' if tipo == 'TE1' else 'Celular'
        
        cursor.execute("""
            INSERT INTO Equipo (numero_serie, marca, modelo, tipo_equipo, codigo_tipo_equipo) 
            VALUES (%s, %s, %s, %s, %s)
        """, (n_serie, marca, modelo, tipo_nombre, tipo))

    print(f"Generando asignaciones aleatorias...")
    # Asignar el 80% de los equipos a usuarios al azar
    num_asignaciones = int(num_records * 0.8)
    for _ in range(num_asignaciones):
        rut = random.choice(rut_generados)
        eq = equipos_generados.pop(random.randint(0, len(equipos_generados)-1))
        fecha_e = fake.date_between(start_date='-2y', end_date='today')
        
        cursor.execute("""
            INSERT INTO AsignacionEquipo (rut_usuario, numero_serie, fecha_entrega) 
            VALUES (%s, %s, %s)
        """, (rut, eq, fecha_e))

    db.commit()
    db.close()
    print("¡Poblamiento masivo completado con éxito!")

if __name__ == "__main__":
    populate_masivo(150)
