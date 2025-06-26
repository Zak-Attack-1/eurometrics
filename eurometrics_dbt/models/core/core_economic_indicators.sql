WITH gdp AS (
    SELECT
        geo      AS country,
        year,
        gdp_eur_millions
    FROM {{ ref('stg_gdp_eurostat') }}
),

hicp AS (
    SELECT
        region   AS country,
        EXTRACT(YEAR FROM date)::int AS year,
        AVG(hicp_index)             AS avg_hicp_index
    FROM {{ ref('stg_hicp_inflation') }}
    GROUP BY country, year
),

pop AS (
    SELECT
        region   AS country,
        year,
        population
    FROM {{ ref('stg_population') }}
)

SELECT
    g.country,
    g.year,
    g.gdp_eur_millions,
    h.avg_hicp_index,
    p.population,
    (g.gdp_eur_millions * 1000000) / p.population AS gdp_per_capita
FROM gdp g
LEFT JOIN hicp h
    ON g.country = h.country
   AND g.year    = h.year
LEFT JOIN pop p
    ON g.country = p.country
   AND g.year    = p.year
ORDER BY g.country, g.year
