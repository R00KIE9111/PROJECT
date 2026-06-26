import pymysql

def run_migration():
    db = pymysql.connect(
        host='eva3-aws-azure-db.c7saowikmas3.us-east-1.rds.amazonaws.com',
        user='admin',
        password='kt7GphhcBsqf.',
        database='project'
    )
    cursor = db.cursor()

    queries = [
        # Pais
        """
        CREATE TABLE IF NOT EXISTS Pais (
            codigo VARCHAR(20) PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL
        );
        """,
        # Modify Ciudad
        """
        ALTER TABLE Ciudad ADD COLUMN id_pais VARCHAR(20);
        """,
        """
        ALTER TABLE Ciudad ADD CONSTRAINT fk_ciudad_pais FOREIGN KEY (id_pais) REFERENCES Pais(codigo);
        """,
        # TipoEquipo
        """
        CREATE TABLE IF NOT EXISTS TipoEquipo (
            codigo VARCHAR(20) PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL
        );
        """,
        # Area
        """
        CREATE TABLE IF NOT EXISTS Area (
            codigo VARCHAR(20) PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            id_empresa INT,
            id_gerente VARCHAR(12),
            FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
        );
        """,
        # Modify Usuario
        """
        ALTER TABLE Usuario 
        ADD COLUMN apellido_paterno VARCHAR(100),
        ADD COLUMN apellido_materno VARCHAR(100),
        ADD COLUMN fecha_nacimiento DATE,
        ADD COLUMN edad INT,
        ADD COLUMN direccion VARCHAR(255),
        ADD COLUMN anexo VARCHAR(20),
        ADD COLUMN email VARCHAR(100),
        ADD COLUMN celular VARCHAR(20),
        ADD COLUMN id_area VARCHAR(20),
        ADD COLUMN oficina VARCHAR(50);
        """,
        """
        ALTER TABLE Usuario ADD CONSTRAINT fk_usuario_area FOREIGN KEY (id_area) REFERENCES Area(codigo);
        """,
        """
        ALTER TABLE Area ADD CONSTRAINT fk_area_gerente FOREIGN KEY (id_gerente) REFERENCES Usuario(rut_usuario);
        """,
        # Modify Equipo
        """
        ALTER TABLE Equipo ADD COLUMN es_reemplazo BOOLEAN DEFAULT FALSE;
        """,
        """
        ALTER TABLE Equipo ADD COLUMN codigo_tipo_equipo VARCHAR(20);
        """,
        """
        ALTER TABLE Equipo ADD CONSTRAINT fk_equipo_tipo FOREIGN KEY (codigo_tipo_equipo) REFERENCES TipoEquipo(codigo);
        """,
        """
        ALTER TABLE Sucursal ADD CONSTRAINT fk_sucursal_empresa FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa);
        """,
        """
        ALTER TABLE Sucursal ADD CONSTRAINT fk_sucursal_ciudad FOREIGN KEY (id_ciudad) REFERENCES Ciudad(id_ciudad);
        """
    ]

    for q in queries:
        try:
            cursor.execute(q)
            db.commit()
            print("Executed:", q.strip())
        except Exception as e:
            print("Error executing:", q.strip())
            print("Error:", e)

    db.close()

if __name__ == "__main__":
    run_migration()
