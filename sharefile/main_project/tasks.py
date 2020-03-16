from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import task
from .models import File
from datetime import datetime as dt
from datetime import date
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour=00)), name="run_every_12", ignore_result=True)
def run_every_12():
	files = File.objects.all()
	for file in files:
		print(file.expiration_date)
		if file.expiration_date < date.today():
			file.is_active = False
			file.save()
	return files
