from persistence_tabla_devolucion import insert_valores_calculo_tabla_devolucion_temp

def main():
    try:
        print("Iniciando el cálculo de la tabla de devolución...")
        # insert_valores_calculo_tabla_devolucion_temp()
        print("Cálculo completado con éxito.")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    main()
