from functools import lru_cache
from logging import Logger, getLogger

import punq
from django.conf import settings
from httpx import Client
from punq import Scope

from apps.keycrm.clients import KeyCRMClient
from apps.keycrm.services import IntegrationService, PipelineService
from apps.keycrm.use_cases import CreateSubscriberToCrmUseCase, LoadAllPipelinesUseCase, UpdateSubscriberToCrmUseCase
from apps.zenedu.clients import ZeneduClient
from apps.zenedu.services import BotService, SubscriberService
from apps.zenedu.use_cases import LoadAllBotsUseCase, LoadAllSubscribersUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(Logger, factory=getLogger, name="django.request")

    def init_zenedu_client():
        return ZeneduClient(
            http_client=Client(base_url="https://app.zenedu.io/"),
            api_key=settings.ZENEDU_API_KEY,
        )

    container.register(ZeneduClient, factory=init_zenedu_client, scope=Scope.singleton)

    def init_keycrm_client():
        return KeyCRMClient(
            http_client=Client(base_url="https://openapi.keycrm.app/v1"),
            api_key=settings.KEYCRM_API_KEY,
        )

    container.register(KeyCRMClient, factory=init_keycrm_client, scope=Scope.singleton)

    container.register(IntegrationService, scope=Scope.singleton)
    container.register(SubscriberService, scope=Scope.singleton)
    container.register(PipelineService, scope=Scope.singleton)
    container.register(BotService, scope=Scope.singleton)

    container.register(LoadAllBotsUseCase, scope=Scope.singleton)
    container.register(LoadAllPipelinesUseCase, scope=Scope.singleton)
    container.register(LoadAllSubscribersUseCase, scope=Scope.singleton)
    container.register(CreateSubscriberToCrmUseCase, scope=Scope.singleton)
    container.register(UpdateSubscriberToCrmUseCase, scope=Scope.singleton)

    return container
