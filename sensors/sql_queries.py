query = """
select
    avg(valorobservado) as average, max(valorobservado) as maximum, 
    min(valorobservado) as minimum, median(valorobservado) as median, 
    codigoestacion, codigosensor, date_trunc_ymd(fechaobservacion), 
    nombreestacion, departamento, municipio, zonahidrografica,
    latitud, longitud
where
    fechaobservacion between '{min_date}T00:00:00.000' and '{max_date}T00:00:00.000'
group by
    codigoestacion, codigosensor, date_trunc_ymd(fechaobservacion), nombreestacion, 
    departamento, municipio, zonahidrografica, latitud, longitud
order by date_trunc_ymd(fechaobservacion)
"""
