from extract_data import *


def test():
    periodo = 20
    print(get_periodos_cobertura())
    print(f"Porcentajes devolución ({periodo}): {get_porcetanje_by_periodo(periodo)}")
    # print(get_porcetanjes_by_periodos())
    valores_tabla_devolucion = get_tabla_devolucion_by_periodo_and_porcentaje()
    # print(valores_tabla_devolucion[periodo][100])
    # print(valores_tabla_devolucion[16])


test()
