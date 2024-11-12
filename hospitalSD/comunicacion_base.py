import mysql.connector


def conectar_base():
    conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sala_emergencia",
    charset="utf8mb4",
    collation="utf8mb4_general_ci",
    auth_plugin="mysql_native_password",  # Especifica el método de autenticación
    use_pure=True  # Fuerza el uso de implementación en Python puro
    )

    return conexion.cursor(), conexion


def lista_tabla(tabla):
    cursor, conexion= conectar_base()
    consulta = f"SELECT i_id_doctor, v_nombre, v_curp FROM {tabla}"
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    for fila in resultados:
        id, nombre, curp= fila
        print(f"ID: {id}, Nombre: {nombre}, CURP: {curp}")
    print(tabla)

    cursor.close()
    conexion.close()

def existe_id(id,tabla):
    cursor, conexion = conectar_base()
    consulta = f"SELECT EXISTS(SELECT 1 FROM {tabla} WHERE i_id_doctor = %s)"

    cursor.execute(consulta, (id,))
    resultados = cursor.fetchall()[0]
    for fila in resultados:
        id = fila
        existe = id
    cursor.close()
    conexion.close()

    if existe == 1:
        print("ID valido")
        return 1
    else:
        print("ID invalido")
        return 0



lista_tabla("tbl_doctores")
