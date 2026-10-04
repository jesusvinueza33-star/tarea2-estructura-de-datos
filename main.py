from shared.herramientas import (
    imprimir_titulo,
    imprimir_color,
    limpiar_pantalla
)
import views


def mostrar_menu():
    """Punto 7: Menú con las opciones requeridas."""
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    print("1. Crear estudiante")
    print("2. Ver todos los estudiantes")
    print("3. Buscar estudiante")
    print("4. Actualizar estudiante")
    print("5. Eliminar estudiante")
    print("6. Agregar nota")
    print("7. Ver promedio")
    print("8. Materias en común")
    print("9. Salir")
    print("-" * 60)


def main():
    opcion = ""
    
    while opcion != "9":
        mostrar_menu()
        opcion = input("Selecciona una opción (1-9): ").strip()

        if opcion == "1":
            views.crear_estudiante()
        elif opcion == "2":
            views.obtener_todos()
        elif opcion == "3":
            views.buscar_estudiantes()
        elif opcion == "4":
            views.actualizar_estudiante()
        elif opcion == "5":
            views.eliminar_estudiante()
        elif opcion == "6":
            views.vista_agregar_nota()
        elif opcion == "7":
            views.vista_ver_promedio()
        elif opcion == "8":
            views.vista_materias_en_comun()
        elif opcion == "9":
            limpiar_pantalla()
            imprimir_color("¡Gracias por usar el sistema de estudiantes!", "VERDE")
        else:
            imprimir_color("Opción no válida. Por favor, intenta de nuevo.", "ROJO")
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()