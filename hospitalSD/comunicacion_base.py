import mysql.connector


def conectar_base():
    conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sala_emergencias",
    charset="utf8mb4",
    collation="utf8mb4_general_ci",
    auth_plugin="mysql_native_password",  # Especifica el método de autenticación
    use_pure=True  # Fuerza el uso de implementación en Python puro
    )

    return conexion.cursor(), conexion

def lista_tabla(tabla): 
    try:
        cursor, conexion= conectar_base()
        if tabla == "tbl_doctores":
            consulta = f"SELECT i_id_doctor, v_nombre, v_curp FROM {tabla}"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                id, nombre, curp= fila
                print(f"ID: {id}, Nombre: {nombre}, CURP: {curp}")
        if tabla == "tbl_pacientes":
            consulta = f"""SELECT 
                            p.i_id_paciente, 
                            p.v_nombre, 
                            p.v_edad, 
                            p.v_emergencia, 
                            v.i_id_sala, 
                            v.i_id_cama, 
                            d.v_nombre,
                            v.b_estatus_visita
                        FROM {tabla} AS p
                        INNER JOIN tbl_visitas AS v ON p.i_id_paciente = v.i_id_paciente
                        INNER JOIN tbl_doctores AS d ON v.i_id_doctor = d.i_id_doctor
                        """
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                id, nombre, edad, emergencia, sala, cama, doctor, estatus = fila
                print(f"ID: {id}, Nombre: {nombre}, Edad: {edad}, Emergencia: {emergencia}, Sala: {sala}, Cama: {cama}, Doctor: {doctor} Estatus: {estatus}")
        if tabla == "tbl_trabajadores_sociales":
            consulta = f"SELECT i_id_sala, v_nombre, v_curp FROM {tabla}"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                id, nombre, curp = fila
                print(f"Sala de emergencia: {id}, Nombre: {nombre}, CURP: {curp}")
        
    except Exception as e: 
        input(f"Ocurrió un error: {e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_tabla(id,campo,tabla,valor):
    try:
        cursor, conexion= conectar_base()
        if tabla == "tbl_doctores":
            consulta = f"UPDATE {tabla} SET {campo} = %s WHERE i_id_doctor = %s"
            cursor.execute(consulta, (valor, id))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Registro actualizado correctamente. Enter para continuar...")
            else:
                print("No se encontró el registro para actualizar. Enter para continuar...")
        if tabla == "tbl_pacientes":
            consulta = f"UPDATE {tabla} SET {campo} = %s WHERE i_id_paciente = %s"
            cursor.execute(consulta, (valor, id))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Registro actualizado correctamente. Enter para continuar...")
            else:
                print("No se encontró el registro para actualizar. Enter para continuar...")
        if tabla == "tbl_trabajadores_sociales":
            consulta = f"UPDATE {tabla} SET {campo} = %s WHERE i_id_sala = %s"
            cursor.execute(consulta, (valor, id))
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

def insertar_en_tabla(valores,tabla):
    try:
        cursor, conexion= conectar_base()
        if tabla == "tbl_doctores":
            nombre = valores[0]
            curp = valores[1]
            print(f"entro a tbl_doctores: {valores}")
            consulta = f"INSERT INTO {tabla} (v_nombre, v_curp) VALUES (%s, %s)"
            cursor.execute(consulta, (nombre,curp,))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Registro exitoso. Seleccione una opcion para continuar...")
            else:
                print("Hubo un problema al registrar al paciente. Seleccione una opcion para continuar...")
        if tabla == "tbl_pacientes":
            print("entra a tbl_pacientes")
            nombre = valores[0]
            edad = valores[1]
            emergencia = valores[2]
            consulta = f"INSERT INTO {tabla} (v_nombre, v_edad, v_emergencia) VALUES (%s, %s,%s)"
            cursor.execute(consulta, (nombre,edad,emergencia,))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Registro exitoso. Seleccione una opcion para continuar...")
            else:
                print("Hubo un problema al registrar al paciente. Enter para continuar...")
        if tabla == "tbl_visitas":
            consulta = f"INSERT INTO {tabla} (i_id_paciente, i_id_doctor, i_id_sala, i_id_cama, v_folio_visita, b_estatus_visita, fecha_visita) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(consulta, (valores[0],valores[1],valores[2],valores[3],valores[4],valores[5],valores[6]))
            conexion.commit()
    except Exception as e:
            input(f"Ocurrió un error: {e}")
    finally:
            cursor.close()
            conexion.close()

def eliminar_en_tabla(id, tabla):
    try:
        cursor, conexion= conectar_base()
        if tabla == "tbl_doctores":
            consulta = f"DELETE FROM {tabla} WHERE i_id_doctor = %s"
            cursor.execute(consulta, (id,))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Registro actualizado correctamente. Enter para continuar...")
            else:
                print("No se encontró el registro para eliminar. Enter para continuar...")
        if tabla == "tbl_pacientes":
            consulta = f"DELETE FROM {tabla} WHERE i_id_paciente = %s"
            cursor.execute(consulta, (id,))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Registro actualizado correctamente. Enter para continuar...")
            else:
                input("No se encontró el registro para eliminar. Enter para continuar...")
            
    except Exception as e:
            input(f"Ocurrió un error: {e}")
    finally:
            cursor.close()
            conexion.close()
    
def existe_id(id,tabla):
    try:
        cursor, conexion = conectar_base()
        if tabla == "tbl_doctores":
            consulta = f"SELECT EXISTS(SELECT 1 FROM {tabla} WHERE i_id_doctor = %s)"
            cursor.execute(consulta, (id,))
            resultados = cursor.fetchall()[0]
            for fila in resultados:
                id = fila
                existe = id
            if existe == 1:
                return 1
            else:
                return 0
        elif tabla == "tbl_pacientes":
            consulta = f"SELECT EXISTS(SELECT 1 FROM {tabla} WHERE i_id_paciente = %s)"
            cursor.execute(consulta, (id,))
            resultados = cursor.fetchall()[0]
            for fila in resultados:
                id = fila
                existe = id
            if existe == 1:
                return 1
            else:
                return 0
        elif tabla == "tbl_trabajadores_sociales":
            consulta = f"SELECT EXISTS(SELECT 1 FROM {tabla} WHERE i_id_sala = %s)"
            cursor.execute(consulta, (id,))
            resultados = cursor.fetchall()[0]
            for fila in resultados:
                id = fila
                existe = id
            if existe == 1:
                return 1
            else:
                return 0

    except Exception as e:
        input(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()

def obtenIdUltimoPaciente():
    try:
        cursor, conexion = conectar_base()
        consulta = "SELECT i_id_paciente FROM tbl_pacientes ORDER BY i_id_paciente DESC LIMIT 1"
        cursor.execute(consulta)
        id_doctor = cursor.fetchone()[0]
    except Exception as e:
        input(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()
    
    return id_doctor

def obtenIdUltimaVisita():
    try:
        cursor, conexion = conectar_base()
        consulta = "SELECT i_id_visita FROM tbl_visitas ORDER BY i_id_visita DESC LIMIT 1"
        cursor.execute(consulta)
        id_visita = cursor.fetchone()[0]
    except Exception as e:
        input(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()

    return id_visita

def obtenSalaDisponible():
    try:
        cursor, conexion = conectar_base()
        consulta= """
                    SELECT i_id_sala_emergencia, i_id_cama, COUNT(*) AS num_camas_desocupadas
                    FROM tbl_camas
                    WHERE b_disponibilidad = 1
                    GROUP BY i_id_sala_emergencia
                    ORDER BY COUNT(*) DESC
                    LIMIT 1;

                    """
        cursor.execute(consulta)
        id_sala = cursor.fetchall()
        consulta2 =f"""
                    UPDATE tbl_camas
                    SET b_disponibilidad = 0
                    WHERE i_id_sala_emergencia = %s AND i_id_cama = %s
                    """
        cursor.execute(consulta2,(int(id_sala[0][0]),int(id_sala[0][1]),))
        conexion.commit()
        return id_sala[0]
    except Exception as e:
        input(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()

def obtenDoctorDisponible():
    try:
        cursor, conexion = conectar_base()
        consulta = """
                    SELECT i_id_doctor
                    FROM tbl_doctores
                    WHERE i_consultas_realizadas = (SELECT MIN(i_consultas_realizadas) FROM tbl_doctores WHERE b_estatus_disponibilidad = 1);
                    """
        cursor.execute(consulta)
        id_doctor = cursor.fetchall()
        consulta2 =f"""
                    UPDATE tbl_doctores
                    SET b_estatus_disponibilidad = 0
                    WHERE i_id_doctor = %s
                    """
        cursor.execute(consulta2,(int(id_doctor[0][0]),))
        consulta3 =f"""
                    UPDATE tbl_doctores
                    SET i_consultas_realizadas = (SELECT i_consultas_realizadas FROM tbl_doctores WHERE i_id_doctor = %s) + 1
                    WHERE i_id_doctor = %s
                    """
        cursor.execute(consulta3,(int(id_doctor[0][0]),int(id_doctor[0][0]),))
        conexion.commit()
        return id_doctor[0][0]
    except Exception as e:
        input(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()

def verificaDisponiblidadDoctor():
    try:
        cursor, conexion = conectar_base()
        consulta = """
                    SELECT i_id_doctor
                    FROM tbl_doctores
                    WHERE b_estatus_disponibilidad = 1
                    """
        cursor.execute(consulta)
        id_doctor = cursor.fetchall()
        if not id_doctor:
            print("No hay doctores disponibles...")
            return 0
        else:
            return 1
    except Exception as e:
        input(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()

def verificaDisponibilidadCama():
    try:
        cursor, conexion = conectar_base()
        consulta = """
                    SELECT i_id_cama
                    FROM tbl_camas
                    WHERE b_disponibilidad = 1
                    """
        cursor.execute(consulta)
        id_camas = cursor.fetchall()
        if not id_camas:
            print("No hay camas disponibles...")
            return 0
        else:
            return 1
    except Exception as e:
        input(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()

def obtenVisitasDoctor(id_doctor):
    try:
        cursor, conexion = conectar_base()
        consulta = f"""SELECT v.v_folio_visita, p.v_nombre, p.v_edad, p.v_emergencia, v.i_id_sala, v.i_id_cama FROM tbl_visitas v
                    INNER JOIN tbl_pacientes p ON v.i_id_paciente = p.i_id_paciente
                    WHERE v.i_id_doctor = %s AND b_estatus_visita = 1"""
        cursor.execute(consulta,(id_doctor,))
        visita = cursor.fetchall()
        if not visita:
            return 0
        else:
            print(f"                        Visita activa\n")
            print(f"Folio:{visita[0][0]} Nombre:{visita[0][1]} Edad:{visita[0][2]} Emergencia:{visita[0][3]} Cama:{visita[0][4]} Sala:{visita[0][5]}\n")
            return visita[0][0]
    except Exception as e:
        input(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()

def cerrarVisitasDoctor(folio):
    try:
        cursor, conexion = conectar_base()
        consulta = f"""UPDATE tbl_visitas
                        SET b_estatus_visita = 0
                        WHERE v_folio_visita = %s"""
        cursor.execute(consulta,(folio,))

        consulta2 = f"""UPDATE tbl_doctores
                        SET b_estatus_disponibilidad = 1
                        WHERE i_id_doctor = (SELECT i_id_doctor FROM tbl_visitas WHERE v_folio_visita = %s)"""
        cursor.execute(consulta2,(folio,))

        consulta3 = f"""UPDATE tbl_camas
                        SET b_disponibilidad = 1
                        WHERE i_id_cama = (SELECT i_id_cama FROM tbl_visitas WHERE v_folio_visita = %s)
                        AND i_id_sala_emergencia = (SELECT i_id_sala FROM tbl_visitas WHERE v_folio_visita = %s) """
        cursor.execute(consulta3,(folio,folio,))
        conexion.commit()
        print("Visita Cerrada. Enter para continuar...")
    except Exception as e:
        print(f"Ocurrió un error{e}. Enter para continuar...")
    finally:
        cursor.close()
        conexion.close()

def moverVisitasDeNodoFallido(salaCaida):
    try:
        cursor, conexion = conectar_base()
        consulta = f"""
                    SELECT v_folio_visita FROM tbl_visitas
                    WHERE i_id_sala = {salaCaida} 
                    AND b_estatus_visita = 1
                    """
        cursor.execute(consulta)
        v_folios = cursor.fetchall()

        consulta2 = f"""
                    SELECT i_id_sala_emergencia, i_id_cama FROM tbl_camas
                    WHERE i_id_sala_emergencia != {salaCaida}
                    AND b_disponibilidad = 1
                    """        
        cursor.execute(consulta2)
        camasDisponibles = cursor.fetchall()

        if len(v_folios) < len(camasDisponibles):
            contador = 0
            for visitas in v_folios:
                consulta3 = f"""UPDATE tbl_visitas
                                SET i_id_sala = {int(camasDisponibles[contador][0])}, i_id_cama = {int(camasDisponibles[contador][1])}
                                WHERE v_folio_visita = '{visitas[0]}'    
                            """    
                print(visitas[0])
                print(camasDisponibles[contador][0])
                print(camasDisponibles[contador][1])
                contador = contador + 1
                cursor.execute(consulta3)
            conexion.commit()
        else:
            print("No es posible cambiar las visitas por falla de nodo. No hay cupo disponible")


        #print(v_folios)
        #print(camasDisponibles)

    except Exception as e:
        print(f"Ocurrió un error{e} Seleccione una opcion: ")
    finally:
        cursor.close()
        conexion.close()


#moverVisitasDeNodoFallido(1)