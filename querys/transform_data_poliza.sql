--356 los registros que se deben modificar en polizar
create table poliza_backup_string as
select p.*
from poliza p
         INNER JOIN poliza_detalle pd
                    USING (id_poliza)
where pd.id_cobertura = 1
  and p.channel = 'VIDA_CASH_PLUS'
  AND p.estado = 3
order by 1 desc;

-- tabla poliza_backup_string:
select *
from poliza_backup_string;

-- update a json valido
UPDATE poliza_backup_string
SET tabla_devolucion = REGEXP_REPLACE(
        REGEXP_REPLACE(
                REPLACE(tabla_devolucion, '=', ':'),
                '([{,]\s*)([0-9]+)(\s*:)', '\1"\2"\3', 'g'
        ),
        ':\s*([0-9.]+)%', ': "\1"', 'g'
                       )
WHERE tabla_devolucion LIKE '%=%';

-- tabla pivote para poliza
-- CREATE TABLE tabla_devolucion_poliza as
create table tabla_devolucion_poliza as
SELECT id_poliza,
       key            as periodo,
       value::NUMERIC as valor
FROM poliza_backup_string, LATERAL json_each_text(tabla_devolucion::JSON);

-- tabla para reformatear el codigo
select tdpo.id_poliza,
       CONCAT('{', STRING_AGG(CONCAT(tdpo.periodo, '=', tdpo.valor, '%'), ', ' ORDER BY CAST(tdpo.periodo AS INTEGER)),
              '}') AS tabla_devolucion
from tabla_devolucion_poliza tdpo
         inner join poliza p on tdpo.id_poliza = p.id_poliza
         inner join poliza_detalle pd on pd.id_poliza = p.id_poliza AND pd.id_cobertura = 1
where p.channel = 'VIDA_CASH_PLUS'
  AND p.estado = 3
GROUP BY tdpo.id_poliza
order by 1 desc;

-- hacer el update en base a la tabla de valores_calculo_tabla_devolucion
select *
from valores_calculo_tabla_devolucion

select *
from poliza_backup_string p
         inner join poliza_detalle pd
                    on p.id_poliza = pd.id_poliza
where p.channel = 'VIDA_CASH_PLUS'
  and p.estado = 3
  and pd.periodo_pago = 8
  and pd.porcentaje_devolucion = 50

-- valores_calculo_tabla_devolucion
-- tabla_devolucion_poliza ya tiene contemplado VIDA_CASH_PLUS
select tdp.*
from tabla_devolucion_poliza tdp
         INNER JOIN poliza p ON p.id_poliza = tdp.id_poliza
         inner join poliza_detalle pd on pd.id_poliza = tdp.id_poliza
-- inner join  valores_calculo_tabla_devolucion
where p.channel = 'VIDA_CASH_PLUS'
  and p.estado = 3
  and tdp.periodo = '1' --vctd.año
  and pd.periodo_pago = '8'
  and pd.porcentaje_devolucion = '50'

-- update para solo polizas
UPDATE tabla_devolucion_poliza tdp
SET valor = vctd.valor
FROM valores_calculo_tabla_devolucion vctd,
     poliza p,
     poliza_detalle pd
WHERE tdp.id_poliza = p.id_poliza
  AND tdp.id_poliza = pd.id_poliza
  AND p.channel = 'VIDA_CASH_PLUS'
  AND p.estado = 3
  AND tdp.periodo::TEXT = vctd.año::TEXT
  AND pd.periodo_pago::TEXT = vctd.periodo::TEXT
  AND pd.porcentaje_devolucion = vctd.porcentaje;


-- validacion de body poliza
SELECT id_poliza,
       CONCAT('{', STRING_AGG(CONCAT('"', periodo, '":"', valor, '"'), ', ' ORDER BY CAST(periodo AS INTEGER)),
              '}') AS tabla_devolucion
FROM tabla_devolucion_poliza
GROUP BY id_poliza;

-- actualizacion masiva poliza
UPDATE poliza p
SET tabla_devolucion = subquery.tabla_devolucion
FROM (SELECT id_poliza,
             CONCAT('{', STRING_AGG(CONCAT('"', periodo, '":"', valor, '"'), ', ' ORDER BY CAST(periodo AS INTEGER)),
                    '}') AS tabla_devolucion
      FROM tabla_devolucion_poliza
      GROUP BY id_poliza) AS subquery
WHERE p.id_poliza = subquery.id_poliza;
-- 356 afectadas


-- validaciones varias

select *
from valores_calculo_tabla_devolucion
where periodo = 12
  and porcentaje = 150


select *, pd.periodo_pago
from poliza p
         inner join poliza_detalle pd on p.id_poliza = pd.id_poliza
where p.id_poliza = 12810

select *
from
    12 - 150


SELECT tdp.*, vctd.valor
FROM tabla_devolucion_poliza tdp
         INNER JOIN valores_calculo_tabla_devolucion vctd ON tdp.periodo = vctd.año
         INNER JOIN poliza p ON p.id_poliza = tdp.id_poliza
         INNER JOIN poliza_detalle pd ON pd.id_poliza = tdp.id_poliza
WHERE p.channel = 'VIDA_CASH_PLUS'
  AND p.estado = '3'
  AND tdp.periodo = 2
  AND pd.periodo_pago = 8
  AND pd.porcentaje_devolucion = 50
order by periodo asc;
