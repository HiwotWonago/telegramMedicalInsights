-- models/staging/stg_telegram_messages.sql

with source as (

    select
        message_id,
        date,
        sender,
        message,
        media_type,
        media_path,
        channel_name,
        json_payload
    from {{ source('raw', 'telegram_message') }}

),

cleaned as (

    select
        message_id,
        date::timestamp as message_timestamp,
        sender,
        channel_name,
        media_type,
        media_path,
        message,
        length(message) as message_length,
        json_payload

    from source

)

select * from cleaned
