import os
from funciones.db import crear_base_de_datos, agregar_paciente, listar_pacientes

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# Comienzo del programa principal
eleccion = "n"
crear_base_de_datos()

while eleccion != "s":
    limpiar_consola()
    print("1 Agregar paciente")
    print("2 Agregar visita")
    print("3 Buscar paciente")
    print("4 Listar pacientes")
    print("s para salir")
    eleccion = input("Ingrese su elección:")
    if(eleccion=="1"):
        limpiar_consola()
        agregar_paciente()
        input("Presione enter para continuar")
    elif(eleccion=="2"):
        limpiar_consola()
        print("Eligió el numero 2")
        input("Presione enter para continuar")
    elif(eleccion=="3"):
        limpiar_consola()
        print("Eligio buscar paciente")
        input("Presione enter para continuar")
    elif(eleccion=="4"):
        limpiar_consola()
        pacientes = listar_pacientes()
        print("Listado de pacientes")
        print("--------------------")
        print()
        for paciente in pacientes:
            print(f"ID: {paciente[0]}, Nombre: {paciente[1]}, Fecha de Nacimiento: {paciente[2]}, Edad: {paciente[3]}, Género: {paciente[4]}")
        print()
        input("Presione enter para continuar")