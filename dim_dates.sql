-- models/dimensions/dim_dates.sql

with date_range as (

    -- Set your desired date range here
    select
        generate_series(
            date '2023-01-01',
            current_date,
            interval '1 day'
        )::date as date

),

final as (

    select
        date as date_id,
        extract(year from date) as year,
        extract(month from date) as month,
        to_char(date, 'Month') as month_name,
        extract(day from date) as day,
        extract(isodow from date) as day_of_week,
        to_char(date, 'Day') as day_name,
        date_trunc('week', date)::date as week_start_date,
        date_trunc('month', date)::date as month_start_date

    from date_range

)

select * from final
