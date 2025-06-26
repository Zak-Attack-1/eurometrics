{{ config(materialized = "view", tags=["staging"]) }}

with source as (

    select *
    from {{ source('eurometrics', 'gdp_eurostat') }}

),

renamed as (

    select
        EXTRACT(YEAR FROM year)::int     as year,
        geo,
        cast(value as numeric)            as gdp_eur_millions
    from source

)

select * from renamed


