import logging

from celery import shared_task

from apps.zenedu.use_cases import LoadAllBotsUseCase, LoadAllSubscribersUseCase
from config.containers import get_container

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def load_all_bots_task(self):
    container = get_container()

    use_case: LoadAllBotsUseCase = container.resolve(LoadAllBotsUseCase)

    try:
        use_case.execute()
    except Exception as e:
        logger.error("Error %s occured while task %s processing", e, self.name)


@shared_task(bind=True)
def load_all_subscribers_task(self):
    container = get_container()

    use_case: LoadAllSubscribersUseCase = container.resolve(LoadAllSubscribersUseCase)

    try:
        use_case.execute()
    except Exception as e:
        logger.error("Error %s occured while task %s processing", e, self.name)
