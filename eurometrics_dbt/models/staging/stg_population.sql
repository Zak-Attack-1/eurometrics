{{ 
  config(
    materialized = "view",
    tags = ["staging"]
  ) 
}}

with raw as (

  select * 
  from {{ source('eurometrics', 'population_data') }}

)

select
  region,
  year::int      as year,
  population::int as population
from raw
