{{ config(materialized = "view", tags=["staging"]) }}

with source as (

    select *
    from {{ source('eurometrics', 'hicp_inflation') }}

),

renamed as (

    select
        date::date as date,
        region,
        cast(hicp_index as numeric) as hicp_index
    from source

)

select * from renamed
