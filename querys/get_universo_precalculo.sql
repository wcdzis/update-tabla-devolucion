-- Ultimo tipo de cambio, en codigo el usado es: 3.718
select distinct tipo_cambio
from precalculo
order by 1 desc;

-- cantidad de periodos que hay para actualizar: 12 periodos diferentes
-- [8, 9, 10, 11, 12, 14, 15, 16, 18, 20, 22, 24]
select distinct periodo_cobertura
from precalculo
where channel = 'VIDA_CASH_PLUS'
  and tipo_cambio = 3.718
  and id_cobertura = 1
  and porcentaje > 0
order by periodo_cobertura ASC;


-- cantidad de porcentajes por periodo
-- TODO: PERIODO 8
select distinct porcentaje
from precalculo
where channel = 'VIDA_CASH_PLUS'
  and tipo_cambio = 3.718
  and id_cobertura = 1
  and porcentaje != 0
  and periodo_cobertura = 20
order by porcentaje ASC;


select tabla_devolucion from precalculo



    -- universo de precalculos:
select *
from precalculo
where channel = 'VIDA_CASH_PLUS'
  and tipo_cambio = 3.718
  and id_cobertura = 1
  and periodo_cobertura = 20
select now()