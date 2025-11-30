import sqlite3
from datetime import datetime, date

db_name='historial_clinico.db'

def calcular_edad(fecha_nacimiento_str):
    # Convertir la fecha de string a objeto date
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
    
    # Fecha actual
    hoy = date.today()
    
    # Calcular la edad
    edad = hoy.year - fecha_nacimiento.year
    
    # Ajustar si todavía no cumplió años este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


def crear_base_de_datos():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Crear tabla pacientes si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            fecha_nacimiento DATE NOT NULL,
            genero TEXT NOT NULL
        )
    ''')
    
    cursor.execute("PRAGMA table_info(pacientes)")
    columnas_existentes = [col[1] for col in cursor.fetchall()]
    
    if 'servicio_medico' not in columnas_existentes:
        try:
            cursor.execute('ALTER TABLE pacientes ADD COLUMN servicio_medico TEXT')
        except sqlite3.OperationalError:
            pass  # Error al agregar columna
    
    if 'obra_social' not in columnas_existentes:
        try:
            cursor.execute('ALTER TABLE pacientes ADD COLUMN obra_social TEXT')
        except sqlite3.OperationalError:
            pass  # Error al agregar columna
    
    # Crear tabla visitas (historial clínico) si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            notas TEXT NOT NULL,
            diagnostico TEXT,
            tratamiento TEXT,
            observaciones TEXT,
            id_paciente INTEGER NOT NULL,
            FOREIGN KEY (id_paciente) REFERENCES pacientes (id)
        )
    ''')
    
    # Agregar nuevas columnas si no existen
    cursor.execute("PRAGMA table_info(visitas)")
    columnas_visitas = [col[1] for col in cursor.fetchall()]
    
    if 'diagnostico' not in columnas_visitas:
        try:
            cursor.execute('ALTER TABLE visitas ADD COLUMN diagnostico TEXT')
        except sqlite3.OperationalError:
            pass
    
    if 'tratamiento' not in columnas_visitas:
        try:
            cursor.execute('ALTER TABLE visitas ADD COLUMN tratamiento TEXT')
        except sqlite3.OperationalError:
            pass
    
    if 'observaciones' not in columnas_visitas:
        try:
            cursor.execute('ALTER TABLE visitas ADD COLUMN observaciones TEXT')
        except sqlite3.OperationalError:
            pass
    
    conn.commit()
    conn.close()

def agregar_paciente():
    print("Agregar paciente")
    print("----------------")
    print()
    nombre = input("Ingrese el nombre del paciente:")
    fecha_nacimiento = input("Ingrese la fecha de nacimiento en formato AAAA-MM-DD:")
    genero = input("Ingrese el género del paciente:")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pacientes (nombre, fecha_nacimiento, genero) VALUES (?,?,?)", (nombre, fecha_nacimiento, genero))

    print()
    print("Paciente agregado con éxito")
    print("ID del paciente:", cursor.lastrowid)
    print("Nombre:",nombre)
    print("Fecha de nacimiento:",fecha_nacimiento)
    print("Edad:", calcular_edad(fecha_nacimiento))
    print("Género:", genero)
    print()
    print()

    conn.commit()
    conn.close()

def listar_pacientes():
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()

    pacientes = cursor.execute("""
        SELECT id, nombre, fecha_nacimiento, 
               (strftime('%Y', 'now') - strftime('%Y', fecha_nacimiento)) - 
               (strftime('%m%d', 'now') < strftime('%m%d', fecha_nacimiento)) AS edad, 
               genero, 
               COALESCE(servicio_medico, 'No especificado') as servicio_medico,
               COALESCE(obra_social, 'No especificado') as obra_social
        FROM pacientes 
        ORDER BY id ASC
    """)
    
    return pacientes.fetchall()

def buscar_pacientes(termino_busqueda):
    """
    Busca pacientes por nombre, género o ID
    """
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    
    # Buscar por nombre (case-insensitive) o por ID si el término es numérico
    termino = f"%{termino_busqueda}%"
    
    query = """
        SELECT id, nombre, fecha_nacimiento, 
               (strftime('%Y', 'now') - strftime('%Y', fecha_nacimiento)) - 
               (strftime('%m%d', 'now') < strftime('%m%d', fecha_nacimiento)) AS edad, 
               genero,
               COALESCE(servicio_medico, 'No especificado') as servicio_medico,
               COALESCE(obra_social, 'No especificado') as obra_social
        FROM pacientes 
        WHERE nombre LIKE ? OR genero LIKE ? OR id = ? OR servicio_medico LIKE ? OR obra_social LIKE ?
        ORDER BY nombre ASC
    """
    
    # Si el término es numérico, intentar buscar por ID
    try:
        id_busqueda = int(termino_busqueda)
    except ValueError:
        id_busqueda = None
    
    if id_busqueda is not None:
        pacientes = cursor.execute(query, (termino, termino, id_busqueda, termino, termino))
    else:
        pacientes = cursor.execute(query, (termino, termino, -1, termino, termino))
    
    return pacientes.fetchall()

def obtener_paciente_por_id(paciente_id):
    """
    Obtiene un paciente por su ID
    """
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    
    cursor.execute("""
        SELECT id, nombre, fecha_nacimiento, 
               (strftime('%Y', 'now') - strftime('%Y', fecha_nacimiento)) - 
               (strftime('%m%d', 'now') < strftime('%m%d', fecha_nacimiento)) AS edad, 
               genero, 
               COALESCE(servicio_medico, 'No especificado') as servicio_medico,
               COALESCE(obra_social, 'No especificado') as obra_social
        FROM pacientes 
        WHERE id = ?
    """, (paciente_id,))
    
    paciente = cursor.fetchone()
    connect.close()
    return paciente

def obtener_historial_clinico(paciente_id):
    """
    Obtiene el historial clínico de un paciente
    """
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    
    cursor.execute("""
        SELECT id, fecha, notas, 
               COALESCE(diagnostico, '') as diagnostico,
               COALESCE(tratamiento, '') as tratamiento,
               COALESCE(observaciones, '') as observaciones
        FROM visitas 
        WHERE id_paciente = ?
        ORDER BY fecha DESC, id DESC
    """, (paciente_id,))
    
    historial = cursor.fetchall()
    connect.close()
    return historial

def agregar_historial_clinico(paciente_id, fecha, notas, diagnostico=None, tratamiento=None, observaciones=None):
    """
    Agrega una entrada al historial clínico de un paciente
    """
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    
    cursor.execute("""
        INSERT INTO visitas (fecha, notas, diagnostico, tratamiento, observaciones, id_paciente)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (fecha, notas, diagnostico, tratamiento, observaciones, paciente_id))
    
    connect.commit()
    visita_id = cursor.lastrowid
    connect.close()
    return visita_id

def eliminar_paciente(paciente_id):
    """
    Elimina un paciente y todo su historial clínico asociado
    Retorna True si se eliminó correctamente, False si no se encontró
    """
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    
    # Primero verificar que el paciente existe
    cursor.execute("SELECT id FROM pacientes WHERE id = ?", (paciente_id,))
    if not cursor.fetchone():
        connect.close()
        return False
    
    # Eliminar primero el historial clínico (visitas)
    cursor.execute("DELETE FROM visitas WHERE id_paciente = ?", (paciente_id,))
    
    # Luego eliminar el paciente
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    
    connect.commit()
    connect.close()
    return True