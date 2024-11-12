import os
import gestion_doctores


def mostrarOpciones():
    opcionMenu = 0
    try:
        while opcionMenu != 3:
            os.system('cls') 
            if opcionMenu > 3:
                input("Seleccione una opción válida. Enter para continuar...")
                os.system('cls')  
            print("         Sala de emergencias 1          \n")
            print("1.Registro visita")
            print("2.Gestionar salas de emergencia")
            print("3.Salir")
            opcionMenu = int(input("Seleccione una opción: "))
            if int(opcionMenu) == 1:
                mostrarOpRegistro()
            if int(opcionMenu) == 2:
                mostrarOpGestion()
    except:
        input("Ingrese un numero correcto. Enter para continuar...")
        mostrarOpciones()

def mostrarOpRegistro():
    opcionMenu = 0
    try:
        nombrePaciente = input("Nombre del paciente: ")
        edadPaciente = int(input("Edad paciente: "))
        descripcionEmergencia = input("Descripción de la emergencia: ")
        insertarEmergencia(nombrePaciente,edadPaciente,descripcionEmergencia)
        mensaje = "Registro finalizado."
    except ValueError:
        mensaje = "Datos erroneos, repita el registro y digite la edad correctamente."
    finally:
        input(f"{mensaje} Enter para continuar...")
    os.system('cls')

def mostrarOpGestion():
    opcionMenu = 0
    try:
        while opcionMenu != 4:
            os.system('cls') 
            if opcionMenu > 3:
                input("Seleccione una opción válida. Enter para continuar...")
                os.system('cls')  
            print("         Gestion de sala de emergencias 1         \n")
            print("1.Doctores")
            print("2.Pacientes")
            print("3.Trabajadores sociales")
            print("4.Salir")
            opcionMenu = int(input("Seleccione una opción: "))
            if int(opcionMenu) == 1:
                gestion_doctores.mostrarOpDoctores()
            if int(opcionMenu) == 2:
                mostrarOpPacientes()
            if int(opcionMenu) == 3:
                mostrarOpTrabajadores()
    except:
        input("Ingrese un numero correcto. Enter para continuar...")
        mostrarOpGestion()

def mostrarOpPacientes():
    os.system('cls') 
    print("Pacientes")
def mostrarOpTrabajadores():
    os.system('cls') 
    print("Trabajadores")

def insertarEmergencia(nombrePaciente,edadPaciente,descripcionEmergencia):
    print("Insertando emergencia")
    
def main():
    mostrarOpciones()



main() 