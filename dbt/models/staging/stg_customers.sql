WITH source AS (

    SELECT *

    FROM {{ ref('customers') }}

),

cleaned AS (

    SELECT

        CAST(customer_id AS INTEGER) AS customer_id,

        CAST(signup_date AS DATE) AS signup_date,

        LOWER(TRIM(experiment_variant)) AS experiment_variant

    FROM source

)

SELECT *

FROM cleaned
