import logging

from celery import shared_task

from apps.keycrm.use_cases import CreateSubscriberToCrmUseCase, LoadAllPipelinesUseCase, UpdateSubscriberToCrmUseCase
from config.containers import get_container

logger = logging.getLogger(__name__)


@shared_task()
def load_all_pipelines_task():
    container = get_container()

    use_case: LoadAllPipelinesUseCase = container.resolve(LoadAllPipelinesUseCase)

    use_case.execute()


@shared_task()
def create_subscriber_to_crm_task(subscriber_id: int, bot_id: int):
    container = get_container()

    use_case: CreateSubscriberToCrmUseCase = container.resolve(CreateSubscriberToCrmUseCase)

    use_case.execute(subscriber_id=subscriber_id, bot_id=bot_id)


@shared_task()
def update_subscriber_to_crm_task(subscriber_id: int, bot_id: int):
    container = get_container()

    use_case: UpdateSubscriberToCrmUseCase = container.resolve(UpdateSubscriberToCrmUseCase)

    use_case.execute(subscriber_id=subscriber_id, bot_id=bot_id)
