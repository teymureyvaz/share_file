from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import task


@periodic_task(run_every=(crontab(hour="9",minute="29")), name="run_every_1_minutes", ignore_result=True)
def return_5():
    return 5


@task
def test():
    return "test"