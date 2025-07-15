from dagster import Definitions
from jobs import medical_insights_job
from schedules import schedules

defs = Definitions(
    jobs=[medical_insights_job],
    schedules=schedules,
)
