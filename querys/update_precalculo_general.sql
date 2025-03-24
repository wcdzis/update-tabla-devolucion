-- Tengo todos los valores recalculados para tabla devolucion en esta entidad que se compone de:
-- periodo | porcentaje | año | valor
select * from valores_calculo_tabla_devolucion;

select * from valores_calculo_tabla_devolucion
where periodo = 8
and porcentaje = 145;

-- Por ejemplo para actualizar sobre el periodo 8, necesitamos obtener los precalculos que son hasta ese periodo con ese porcentaje
select * from precalculo
         where channel = 'VIDA_CASH_PLUS'
           and     tipo_cambio = 3.718
           and     id_cobertura = 1
           and periodo_cobertura = 8
           and porcentaje = 50;

select id_precalculo from precalculo
where channel = 'VIDA_CASH_PLUS'
  and     tipo_cambio = 3.718
  and     id_cobertura = 1
  and periodo_cobertura = 8
  and porcentaje = 50;

-- Tengo una tabla donde almaceno todos los valores distribuidos en tabla_devolucion
select * from tabla_devolucion_precalculo
where CAST(periodo AS INT) = 8
and id_precalculo in (select id_precalculo from precalculo
                     where channel = 'VIDA_CASH_PLUS'
                       and     tipo_cambio = 3.718
                       and     id_cobertura = 1)
and valor <= (
    select valor from valores_calculo_tabla_devolucion
    where periodo = 8
      and porcentaje = 50
    order by 1 desc
    limit 1)
order by valor asc

-- es para 8 con 50
SELECT tdp.*, vctd.año
FROM tabla_devolucion_precalculo tdp
         INNER JOIN precalculo p ON p.id_precalculo = tdp.id_precalculo
         INNER JOIN (
    SELECT MAX(valor) AS valor
    FROM valores_calculo_tabla_devolucion vctd
    WHERE periodo = 8 AND porcentaje = 50
) vc ON tdp.valor <= vc.valor
WHERE CAST(tdp.periodo  AS INT)  = '8'
  AND p.channel = 'VIDA_CASH_PLUS'
  AND p.tipo_cambio = 3.718
  AND p.id_cobertura = 1
ORDER BY tdp.valor ASC;

SELECT tdp.*,
FROM tabla_devolucion_precalculo tdp
         INNER JOIN precalculo p ON p.id_precalculo = tdp.id_precalculo
         INNER JOIN (
    SELECT MAX(valor) AS valor
    FROM valores_calculo_tabla_devolucion
    WHERE periodo = 8 AND porcentaje = 50
) vc ON tdp.valor <= vc.valor
WHERE CAST(tdp.periodo AS INT) = 8
  AND p.channel = 'VIDA_CASH_PLUS'
  AND p.tipo_cambio = 3.718
  AND p.id_cobertura = 1
ORDER BY tdp.valor ASC;


SELECT tdp.*, vctd.año
FROM tabla_devolucion_precalculo tdp
         INNER JOIN precalculo p ON p.id_precalculo = tdp.id_precalculo
         INNER JOIN (
    SELECT MAX(valor) AS valor
    FROM valores_calculo_tabla_devolucion
    WHERE periodo = 20
      AND porcentaje = 50
) vc ON tdp.valor <= vc.valor
         INNER JOIN valores_calculo_tabla_devolucion vctd ON vctd.periodo = tdp.periodo
    AND vctd.valor = tdp.valor
WHERE  p.channel = 'VIDA_CASH_PLUS'
  AND p.tipo_cambio = 3.718
  AND p.id_cobertura = 1
  AND vctd.periodo = 20 -- variable
-- AND vctd.año = 3 -- variable
AND vctd.porcentaje = 50 -- variable
ORDER BY vctd.año ASC;


select * from precalculo where
                             channel = 'VIDA_CASH_PLUS'
and tipo_cambio = 3.718
and id_cobertura = 1
and periodo_cobertura = 20

select * from tabla_devolucion_precalculo where id_precalculo in (
    select precalculo.id_precalculo from precalculo where
        channel = 'VIDA_CASH_PLUS'
                               and tipo_cambio = 3.718
                               and id_cobertura = 1
                               and periodo_cobertura = 20
    )
                                          and periodo <= 20
                                            and precalculo.porcentaje = 50
                                          and periodo = 1 -- (año por parte de mi tabla)
order by periodo asc


-- para 20
SELECT tdp.id_precalculo, tdp.periodo, tdp.valor
FROM tabla_devolucion_precalculo tdp
    INNER JOIN precalculo p ON tdp.id_precalculo = p.id_precalculo
WHERE p.channel = 'VIDA_CASH_PLUS'
  AND p.tipo_cambio = 3.718
  AND p.id_cobertura = 1
  -- where update
  AND tdp.periodo <= 15 -- variable
  AND p.periodo_cobertura = 15 -- variable
  AND p.porcentaje = 160 -- variable

ORDER BY tdp.periodo ASC;

(0.0, 1, 15, 160),

-- periodo y año cuadran


-- cambio a int
DO $$
    BEGIN
        ALTER TABLE tabla_devolucion_precalculo
            ALTER COLUMN periodo TYPE INTEGER USING periodo::INTEGER;
    EXCEPTION
        WHEN others THEN
            RAISE NOTICE 'Error: %', SQLERRM;
    END $$;
SELECT * FROM pg_stat_activity WHERE state = 'active';


SELECT
    id_precalculo,
    CONCAT('{', STRING_AGG(CONCAT(periodo, '=', valor, '%'), ', ' ORDER BY CAST(periodo AS INTEGER)), '}') AS tabla_devolucion
FROM
    tabla_devolucion_precalculo
GROUP BY
    id_precalculo;


-- este query es el que genera la correcta correcta
SELECT
    tdp.id_precalculo,
    CONCAT('{', STRING_AGG(CONCAT(tdp.periodo, '=', tdp.valor, '%'), ', ' ORDER BY CAST(tdp.periodo AS INTEGER)), '}') AS tabla_devolucion
FROM
    tabla_devolucion_precalculo tdp
        INNER JOIN
    precalculo p ON tdp.id_precalculo = p.id_precalculo
WHERE
    p.channel = 'VIDA_CASH_PLUS'
  AND p.tipo_cambio = 3.718
  AND p.id_cobertura = 1
and p.periodo_cobertura >= 8
and p.porcentaje > 0
GROUP BY
    tdp.id_precalculo;

-- select * from precalculo where periodo_cobertura = 20;


-- update del precalculo
UPDATE precalculo p
SET tabla_devolucion = subquery.tabla_devolucion
FROM (
         SELECT
             tdp.id_precalculo,
             CONCAT('{', STRING_AGG(CONCAT(tdp.periodo, '=', tdp.valor, '%'), ', ' ORDER BY CAST(tdp.periodo AS INTEGER)), '}') AS tabla_devolucion
         FROM
             tabla_devolucion_precalculo tdp
                 INNER JOIN precalculo p2 ON tdp.id_precalculo = p2.id_precalculo
         WHERE
             p2.channel = 'VIDA_CASH_PLUS'
           AND p2.tipo_cambio = 3.718
           AND p2.id_cobertura = 1
           AND p2.periodo_cobertura BETWEEN 8 AND 20
           AND p2.porcentaje > 0
         GROUP BY
             tdp.id_precalculo
     ) AS subquery
WHERE p.id_precalculo = subquery.id_precalculo;
