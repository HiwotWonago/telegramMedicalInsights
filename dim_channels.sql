-- models/dimensions/dim_channels.sql

with source as (

    select * from {{ ref('stg_telegram_messages') }}

),

channels as (

    select
        channel_name,
        min(message_timestamp) as first_message_time,
        max(message_timestamp) as latest_message_time,
        count(*) as total_messages,
        count(case when media_type is not null then 1 end) as media_messages

    from source
    group by channel_name

)

select * from channels
