import logging
from dataclasses import dataclass
from logging import Logger

from apps.keycrm.clients import KeyCRMClient
from apps.keycrm.entities import Client, Lead
from apps.keycrm.services import IntegrationService, PipelineService
from apps.zenedu.services import SubscriberService

logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class LoadAllPipelinesUseCase:
    pipeline_service: PipelineService
    keycrm_client: KeyCRMClient

    def execute(self):
        pipelines = self.keycrm_client.get_all_pipelines(limit=50)
        logger.info("Received %s pipelines", len(pipelines))

        for pipeline in pipelines:
            _, is_created = self.pipeline_service.create_or_update(pipeline=pipeline)

            if is_created:
                logger.info("Pipeline %s has been created", pipeline.name)
            else:
                logger.info("Pipeline %s has been updated", pipeline.name)


@dataclass(frozen=True, eq=False)
class CreateSubscriberToCrmUseCase:
    subscriber_service: SubscriberService
    integration_service: IntegrationService
    keycrm_client: KeyCRMClient

    def execute(self, subscriber_id: int, bot_id: int):
        subscriber = self.subscriber_service.get_by_id(subscriber_id=subscriber_id)
        integrations = self.integration_service.get_all_by_bot_id(bot_id=bot_id)

        if not subscriber:
            logger.warning("There is no subscriber by id: %s", subscriber_id)
            return

        if not integrations:
            logger.warning("There is no integrations with bot id: %s", bot_id)
            return

        for integration in integrations:
            if not integration.is_active:
                return

            client = Client(
                full_name=" ".join([value for value in [subscriber.first_name, subscriber.last_name] if value]),
                phones=[subscriber.phone],
                username=subscriber.username,
            )
            received_client = self.keycrm_client.create_client(client=client)
            logger.info("Clint %s has been created successfuly", received_client.id)

            lead = Lead(
                client_id=received_client.id,
                pipeline_id=integration.pipeline_id,
            )
            received_lead = self.keycrm_client.create_lead(lead=lead)
            logger.info("Lead %s has been created successfuly", received_lead.id)

            self.subscriber_service.partial_update(subscriber_id=subscriber_id, source_id=received_client.id)
            logger.info("Subscriber %s source id %s has been updated successfuly", subscriber_id, received_client.id)


@dataclass(frozen=True, eq=False)
class UpdateSubscriberToCrmUseCase:
    subscriber_service: SubscriberService
    integration_service: IntegrationService
    keycrm_client: KeyCRMClient
    logger: Logger

    def execute(self, subscriber_id: int, bot_id: int):
        subscriber = self.subscriber_service.get_by_id(subscriber_id=subscriber_id)
        integration = self.integration_service.get_all_by_bot_id(bot_id=bot_id)

        if not subscriber:
            logger.warning("There is no subscriber by id: %s", subscriber_id)
            return

        if not integration:
            logger.warning("There is no integration with bot id: %s", bot_id)
            return

        if not integration.is_active:
            return

        received_client = self.keycrm_client.get_client_by_id(client_id=subscriber.source_id)

        if not received_client:
            logger.warning("There is no client by id: %s", subscriber.source_id)
            return

        logger.info("Clint %s has been received successfuly", received_client.id)

        received_client.phones = [] if received_client.phones else [subscriber.phone]
        received_client.username = None if received_client.username else subscriber.username

        self.keycrm_client.update_client(client=received_client)
        logger.info("Clint %s has been updated successfuly", received_client.id)
