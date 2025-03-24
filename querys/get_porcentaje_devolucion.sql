CREATE OR REPLACE FUNCTION get_porcentaje_devolucion(p_periodo INTEGER, p_tipo_cambio NUMERIC)
    RETURNS TABLE(porcentaje NUMERIC) AS $$
BEGIN
    RETURN QUERY
        SELECT DISTINCT p.porcentaje::NUMERIC
        FROM precalculo p
        WHERE p.channel = 'VIDA_CASH_PLUS'
          AND p.tipo_cambio = p_tipo_cambio
          AND p.id_cobertura = 1
          AND p.porcentaje > 0
          AND p.periodo_cobertura = p_periodo;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_porcentaje_devolucion(8, 3.718);
