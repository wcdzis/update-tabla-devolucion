-- 354568
-- 4472 8 - 50%
-- ...
-- ...

select  count(1)
from    precalculo
where   channel = 'VIDA_CASH_PLUS'
  and     tipo_cambio = 3.718
  and     id_cobertura = 1
  and     periodo_cobertura = 8
  and     porcentaje = 50


create table precalculo_backup_json as
select  *
from    precalculo
where   channel = 'VIDA_CASH_PLUS'
  and     tipo_cambio = 3.718
  and     id_cobertura = 1


select  *
from    precalculo_backup

select  *
from    precalculo_backup_json
limit 1000


UPDATE precalculo_backup_json
SET tabla_devolucion = REGEXP_REPLACE(
        REGEXP_REPLACE(
                REPLACE(tabla_devolucion, '=', ':'),
                '([{,]\s*)([0-9]+)(\s*:)', '\1"\2"\3', 'g'
        ),
        ':\s*([0-9.]+)%', ': "\1"', 'g'
                       )
WHERE tabla_devolucion LIKE '%=%';


create table tabla_devolucion_precalculo as
SELECT id_precalculo,
       key AS periodo,
       value::NUMERIC AS valor
FROM
    precalculo_backup_json,
    LATERAL json_each_text(tabla_devolucion::JSON)



update  tabla_devolucion_precalculo td
set     valor = XXXX
    inner join  precalculo p
  on    td.id_precalculo = p.id_precalculo
where   p.periodo = 8
and     porcentaje = 50


    -- periodo es diferente a periodo de cobertura
select  *
from    tabla_devolucion_precalculo td
inner join precalculo p
on td.id_precalculo = p.id_precalculo
where p.periodo_cobertura = 8
limit 100

-- ESTOS SON LOS VALORES A ACTUALIZAR
-- 4453 de periodo 8
select  td.periodo, td.valor
from tabla_devolucion_precalculo td
            inner join precalculo p
                       on td.id_precalculo = p.id_precalculo
where p.periodo_cobertura = 8
and p.porcentaje = 50
and CAST(td.periodo AS INT) <= p.periodo_cobertura ;

select * from tabla_devolucion_precalculo

SELECT
    CAST(td.periodo AS INT) AS periodo_precalculo,
    td.valor AS valor_precalculo,
    vcd.año AS año_valores,
    vcd.valor AS valor_valores
FROM tabla_devolucion_precalculo td
         INNER JOIN precalculo p ON td.id_precalculo = p.id_precalculo
         INNER JOIN valores_calculo_tabla_devolucion vcd
                    ON p.periodo_cobertura = 8
                        AND p.porcentaje = 50
                        AND vcd.año = CAST(td.periodo AS INT)
WHERE CAST(td.periodo AS INT) <= p.periodo_cobertura
  and channel = 'VIDA_CASH_PLUS'
  and     tipo_cambio = 3.718
  and     id_cobertura = 1
;




-- NECESITO UNA TABLA TERMPORAL DONDE GUARDAR LA DATA DE CALCULO_TABLA_DEVOLUCION
-- periodo | porcentaje | año | valor
-- 8 | 50 | 1 | 0
-- 8 | 50 | 2 | 0.025
-- 8 | 50 | 3 | 0.025
-- 8 | 50 | 4 | 0.025
-- 8 | 50 | 5 | 0.025
-- 8 | 50 | 6 | 0.025
-- 8 | 50 | 7 | 0.025
-- 8 | 50 | 8 | 0.5
select * from valores_calculo_tabla_devolucion;

--


select  *
from    tabla_devolucion_precalculo
where   id_precalculo = 12643671



1 = 0.0625
2 = 0.0625
3 = 0.0625
4 = 0.0625
5 = 0.0625
6 = 0.0625
8 = 1.25