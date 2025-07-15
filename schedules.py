from dagster import ScheduleDefinition
from .jobs import medical_insights_job

daily_schedule = ScheduleDefinition(
    job=medical_insights_job,
    cron_schedule="0 9 * * *",  # daily at 9:00 AM
)

schedules = [daily_schedule]
