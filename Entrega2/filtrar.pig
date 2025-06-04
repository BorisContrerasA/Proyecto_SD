datos = LOAD 'tiempo*.csv' USING PigStorage(',') AS (
    city:chararray,
    subtype:chararray,
    type:chararray,
    x:double,
    y:double,
    timestamp:chararray
);
-- Filtrar vacíos
limpios = FILTER datos BY city != '' AND subtype != '' AND type != '';

-- Agrupar
agrupados = GROUP limpios BY (city, type);

-- Contar 
conteo = FOREACH agrupados GENERATE
    FLATTEN(group) AS (city:chararray, type:chararray),
    COUNT(limpios) AS cantidad;

-- Mostrar
DUMP conteo;

-- Guardar
STORE conteo INTO 'resultados/conteo_ciudadytipo.csv' USING PigStorage(',') PARALLEL 1;