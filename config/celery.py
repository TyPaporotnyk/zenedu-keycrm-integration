from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app = Celery("zenedu-keycrm-integration")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
