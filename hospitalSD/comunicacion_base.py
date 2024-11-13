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
    if tabla == "tbl_doctores":
        consulta = f"SELECT i_id_doctor, v_nombre, v_curp FROM {tabla}"
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        for fila in resultados:
            id, nombre, curp= fila
            print(f"ID: {id}, Nombre: {nombre}, CURP: {curp}")
    cursor.close()
    conexion.close()

def actualizar_tabla(id,campo,tabla,valor):
    if tabla == "tbl_doctores":
        try:
            cursor, conexion= conectar_base()
            consulta = f"UPDATE {tabla} SET {campo} = %s WHERE i_id_doctor = %s"
            cursor.execute(consulta, (valor, id))
            conexion.commit()
            if cursor.rowcount > 0:
                input("Registro actualizado correctamente. Enter para continuar...")
            else:
                input("No se encontró el registro para actualizar. Enter para continuar...")
            
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        finally:
            cursor.close()
            conexion.close()

def insertar_en_tabla(valores,tabla):
    if tabla == "tbl_doctores":
        try:
            cursor, conexion= conectar_base()
            nombre = valores[0]
            curp = valores[1]
            consulta = f"INSERT INTO {tabla} (v_nombre, v_curp) VALUES (%s, %s)"
            cursor.execute(consulta, (nombre,curp,))
            conexion.commit()
            if cursor.rowcount > 0:
                input("Registro actualizado correctamente. Enter para continuar...")
            else:
                input("No se encontró el registro para actualizar. Enter para continuar...")
            
        except Exception as e:
            input(f"Ocurrió un error: {e}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_en_tabla(id, tabla):
    if tabla == "tbl_doctores":
        try:
            cursor, conexion= conectar_base()
            consulta = f"DELETE FROM {tabla} WHERE i_id_doctor = %s"
            cursor.execute(consulta, (id,))
            conexion.commit()
            if cursor.rowcount > 0:
                input("Registro actualizado correctamente. Enter para continuar...")
            else:
                input("No se encontró el registro para eliminar. Enter para continuar...")
            
        except Exception as e:
            input(f"Ocurrió un error: {e}")
        finally:
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
        return 1
    else:
        return 0


