-- actualizacion masiva poliza
UPDATE poliza p
SET tabla_devolucion = subquery.tabla_devolucion
FROM (
         SELECT
             id_poliza,
             CONCAT('{', STRING_AGG(CONCAT('"', periodo, '":"', valor, '"'), ', ' ORDER BY CAST(periodo AS INTEGER)), '}') AS tabla_devolucion
         FROM
             tabla_devolucion_poliza
         GROUP BY
             id_poliza
     ) AS subquery
WHERE p.id_poliza = subquery.id_poliza;
-- 356 afectadas
