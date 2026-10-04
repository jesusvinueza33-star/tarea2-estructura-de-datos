import os
from shared.json_manager import GestorJSON
from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_color,
    limpiar_pantalla
)
from models import Estudiante

# Punto 2: Gestor apuntando a data/estudiantes.json
GESTOR = GestorJSON("data/estudiantes.json")


def cargar_estudiantes():
    """Lee el JSON y devuelve una lista con objetos Estudiante."""
    datos_json = GESTOR.leer()
    estudiantes = []
    for dato in datos_json:
        estudiante = Estudiante.desde_diccionario(dato)
        estudiantes.append(estudiante)
    return estudiantes


def guardar_estudiantes(estudiantes):
    """Guarda la lista de estudiantes en el JSON."""
    lista_diccionarios = []
    for est in estudiantes:
        lista_diccionarios.append(est.a_diccionario())
    GESTOR.guardar(lista_diccionarios)


# --- LAS 5 OPERACIONES BÁSICAS ---

def crear_estudiante():
    """Punto 2 y 3: Crea un nuevo estudiante validando que el carnet no se repita."""
    imprimir_titulo("CREAR ESTUDIANTE")
    estudiantes = cargar_estudiantes()

    # Punto 3: Usar un set para validar que el carnet no se repita
    carnets_existentes = set()
    for est in estudiantes:
        carnets_existentes.add(est.carnet)

    carnet = input("Ingresa el carnet: ").strip()
    if carnet in carnets_existentes:
        imprimir_color("Error: Ya existe un estudiante registrado con ese carnet.", "ROJO")
        input("\nPresiona Enter para continuar...")
        return

    nombre = input("Ingresa el nombre: ").strip()
    apellido = input("Ingresa el apellido: ").strip()
    email = input("Ingresa el email: ").strip()

    nuevo_id = len(estudiantes) + 1
    nuevo_estudiante = Estudiante(nuevo_id, nombre, apellido, email, carnet)
    estudiantes.append(nuevo_estudiante)

    guardar_estudiantes(estudiantes)
    imprimir_exito("Estudiante registrado con éxito.")
    input("\nPresiona Enter para continuar...")


def obtener_todos():
    """Punto 2: Muestra la lista de todos los estudiantes."""
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = cargar_estudiantes()

    if not estudiantes:
        print("No hay estudiantes registrados.")
    else:
        for est in estudiantes:
            print(f"ID: {est.id} | Carnet: {est.carnet} | Nombre: {est.obtener_nombre_completo()} | Email: {est.email}")
            if est.materias:
                print(f"   Materias: {', '.join(sorted(est.materias))}")
            print("-" * 50)

    input("\nPresiona Enter para continuar...")


def buscar_estudiantes():
    """Punto 2: Busca estudiantes por nombre, apellido o carnet."""
    imprimir_titulo("BUSCAR ESTUDIANTE")
    estudiantes = cargar_estudiantes()
    busqueda = input("Ingresa el nombre, apellido o carnet a buscar: ").strip().lower()

    encontrados = []
    for est in estudiantes:
        if (busqueda in est.nombre.lower() or 
            busqueda in est.apellido.lower() or 
            busqueda in est.carnet.lower()):
            encontrados.append(est)

    if not encontrados:
        imprimir_color("No se encontraron coincidencias.", "ROJO")
    else:
        for est in encontrados:
            print(f"ID: {est.id} | Carnet: {est.carnet} | Nombre: {est.obtener_nombre_completo()} | Email: {est.email}")
            print("-" * 50)

    input("\nPresiona Enter para continuar...")


def actualizar_estudiante():
    """Punto 2: Actualiza los datos de un estudiante."""
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    estudiantes = cargar_estudiantes()
    carnet_buscar = input("Ingresa el carnet del estudiante a actualizar: ").strip()

    estudiante_encontrado = None
    for est in estudiantes:
        if est.carnet == carnet_buscar:
            estudiante_encontrado = est
            break

    if not estudiante_encontrado:
        imprimir_color("Estudiante no encontrado.", "ROJO")
    else:
        nuevo_nombre = input(f"Nuevo nombre ({estudiante_encontrado.nombre}): ").strip()
        nuevo_apellido = input(f"Nuevo apellido ({estudiante_encontrado.apellido}): ").strip()
        nuevo_email = input(f"Nuevo email ({estudiante_encontrado.email}): ").strip()

        if nuevo_nombre:
            estudiante_encontrado.nombre = nuevo_nombre
        if nuevo_apellido:
            estudiante_encontrado.apellido = nuevo_apellido
        if nuevo_email:
            estudiante_encontrado.email = nuevo_email

        guardar_estudiantes(estudiantes)
        imprimir_exito("Estudiante actualizado correctamente.")

    input("\nPresiona Enter para continuar...")


def eliminar_estudiante():
    """Punto 2: Elimina un estudiante por su carnet."""
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    estudiantes = cargar_estudiantes()
    carnet_buscar = input("Ingresa el carnet del estudiante a eliminar: ").strip()

    estudiante_encontrado = None
    for est in estudiantes:
        if est.carnet == carnet_buscar:
            estudiante_encontrado = est
            break

    if not estudiante_encontrado:
        imprimir_color("Estudiante no encontrado.", "ROJO")
    else:
        estudiantes.remove(estudiante_encontrado)
        guardar_estudiantes(estudiantes)
        imprimir_exito("Estudiante eliminado correctamente.")

    input("\nPresiona Enter para continuar...")


# --- FUNCIONES ADICIONALES PEDIDAS EN LA TAREA ---

def agregar_nota(id_estudiante, materia, nota):
    """Punto 4: Agrega nota entre 0 y 20; retorna (bool, mensaje)."""
    if nota < 0 or nota > 20:
        return False, "La nota debe estar entre 0 y 20."

    estudiantes = cargar_estudiantes()
    estudiante_encontrado = None
    for est in estudiantes:
        if str(est.id) == id_estudiante or est.carnet.lower() == str(id_estudiante).lower():
            estudiante_encontrado = est
            break

    if not estudiante_encontrado:
        return False, "Estudiante no encontrado."

    estudiante_encontrado.agregar_nota(materia, nota)
    guardar_estudiantes(estudiantes)
    return True, "Nota agregada exitosamente."


def materias_ofertadas():
    """Punto 5: Devuelve el set con todas las materias inscritas sin repetir."""
    estudiantes = cargar_estudiantes()
    todas_las_materias = set()
    for est in estudiantes:
        for materia in est.materias:
            todas_las_materias.add(materia)
    return todas_las_materias


def estudiantes_en_comun(id_a, id_b):
    """Punto 6: Usa intersección de conjuntos (&) entre dos estudiantes."""
    estudiantes = cargar_estudiantes()
    est_a = None
    est_b = None

    for est in estudiantes:
        if str(est.id) == str(id_a) or est.carnet == str(id_a):
            est_a = est
        if str(est.id) == str(id_b) or est.carnet == str(id_b):
            est_b = est

    if not est_a or not est_b:
        return None

    # Intersección utilizando la función nativa del modelo o directamente el operador &
    return est_a.materias_en_comun(est_b)


# --- INTERFACES PARA LLAMAR A LAS FUNCIONES ESPECIALES DESDE EL MENÚ ---

def vista_agregar_nota():
    imprimir_titulo("AGREGAR NOTA A ESTUDIANTE")
    id_est = input("Ingresa el ID o Carnet del estudiante: ").strip()
    materia = input("Ingresa el nombre de la materia: ").strip()
    try:
        nota = float(input("Ingresa la nota (0 - 20): "))
        exito, mensaje = agregar_nota(id_est, materia, nota)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_color(f"Error: {mensaje}", "ROJO")
    except ValueError:
        imprimir_color("La nota debe ser un número.", "ROJO")

    input("\nPresiona Enter para continuar...")


def vista_ver_promedio():
    imprimir_titulo("VER PROMEDIO DE ESTUDIANTE")
    id_est = input("Ingresa el ID o Carnet del estudiante: ").strip()
    estudiantes = cargar_estudiantes()
    
    encontrado = None
    for est in estudiantes:
        if str(est.id) == id_est or est.carnet == id_est:
            encontrado = est
            break

    if encontrado:
        promedio = encontrado.obtener_promedio()
        print(f"\nEstudiante: {encontrado.obtener_nombre_completo()}")
        print(f"Promedio general: {promedio}")
    else:
        imprimir_color("Estudiante no encontrado.", "ROJO")

    input("\nPresiona Enter para continuar...")


def vista_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN ENTRE DOS ESTUDIANTES")
    id_a = input("Ingresa el ID o Carnet del primer estudiante: ").strip()
    id_b = input("Ingresa el ID o Carnet del segundo estudiante: ").strip()

    coincidencias = estudiantes_en_comun(id_a, id_b)

    if coincidencias is None:
        imprimir_color("No se pudo encontrar a uno o ambos estudiantes.", "ROJO")
    elif len(coincidencias) == 0:
        print("\nLos estudiantes no comparten ninguna materia.")
    else:
        print(f"\nMaterias en común ({len(coincidencias)}):")
        for mat in coincidencias:
            print(f" - {mat}")

    input("\nPresiona Enter para continuar...")