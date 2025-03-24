CREATE OR REPLACE PROCEDURE actualizar_tablas_devolucion()
    LANGUAGE plpgsql
AS
$$
BEGIN
    -- Actualización para la tabla 'precalculo'
    UPDATE precalculo p
    SET tabla_devolucion = subquery.tabla_devolucion
    FROM (SELECT tdp.id_precalculo,
                 CONCAT('{', STRING_AGG(CONCAT(tdp.periodo, '=', tdp.valor, '%'), ', '
                                        ORDER BY CAST(tdp.periodo AS INTEGER)), '}') AS tabla_devolucion
          FROM tabla_devolucion_precalculo tdp
                   INNER JOIN precalculo p2 ON tdp.id_precalculo = p2.id_precalculo
          WHERE p2.channel = 'VIDA_CASH_PLUS'
            AND p2.tipo_cambio = 3.718
            AND p2.id_cobertura = 1
            AND p2.periodo_cobertura BETWEEN 8 AND 20
            AND p2.porcentaje > 0
          GROUP BY tdp.id_precalculo) AS subquery
    WHERE p.id_precalculo = subquery.id_precalculo;

    -- Actualización para la tabla 'poliza'
    UPDATE poliza p
    SET tabla_devolucion = subquery.tabla_devolucion
    FROM (SELECT id_poliza,
                 CONCAT('{',
                        STRING_AGG(CONCAT('"', periodo, '":"', valor, '"'), ', ' ORDER BY CAST(periodo AS INTEGER)),
                        '}') AS tabla_devolucion
          FROM tabla_devolucion_poliza
          GROUP BY id_poliza) AS subquery
    WHERE p.id_poliza = subquery.id_poliza;

    RAISE NOTICE 'Actualización completada correctamente.';
END;
$$;

