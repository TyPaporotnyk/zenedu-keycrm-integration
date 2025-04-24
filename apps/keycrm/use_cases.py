import logging
from dataclasses import dataclass

from apps.keycrm.clients import KeyCRMClient
from apps.keycrm.entities import Client, Lead, Payment
from apps.keycrm.services import IntegrationService, PipelineService
from apps.keycrm.utils import get_payment_description
from apps.zenedu.services import BotService, OrderService, SubscriberService

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
    order_service: OrderService
    integration_service: IntegrationService
    keycrm_client: KeyCRMClient
    bot_service: BotService

    def execute(self, subscriber_id: int, bot_id: int, order_id: int | None):
        subscriber = self.subscriber_service.get_by_id(subscriber_id=subscriber_id)
        integrations = self.integration_service.get_all_by_bot_id(bot_id=bot_id)
        bot = self.bot_service.get_by_id(bot_id=bot_id)
        order = self.order_service.get_by_id(order_id=order_id) if order_id else None

        if not subscriber:
            logger.warning("There is no subscriber by id: %s", subscriber_id)
            return

        if not integrations:
            logger.warning("There is no integrations with bot id: %s", bot_id)
            return

        for integration in integrations:
            if not integration.is_active:
                continue

            if not subscriber.source_id:
                client = Client(
                    full_name=" ".join([value for value in [subscriber.first_name, subscriber.last_name] if value]),
                    phone=subscriber.phone,
                    username=subscriber.username,
                )
                received_client = self.keycrm_client.create_client(client=client)
                logger.info("Clint %s has been created successfuly", received_client.id)

                self.subscriber_service.partial_update(subscriber_id=subscriber_id, source_id=received_client.id)
                subscriber.source_id = received_client.id
                logger.info(
                    "Subscriber %s source id %s has been updated successfuly", subscriber_id, received_client.id
                )

            lead = Lead(
                title=f"Подписчик {bot.name}",
                client_id=subscriber.source_id,
                pipeline_id=integration.pipeline_id,
                bot=bot.name,
            )
            received_lead = self.keycrm_client.create_lead(lead=lead)
            logger.info("Lead %s has been created successfuly", received_lead.id)

            if order:
                payment = Payment(
                    amount=order.price,
                    status="paid",
                    payment_date=order.created_at,
                    description=get_payment_description(subscriber=subscriber, bot=bot),
                )
                self.keycrm_client.add_payment_to_lead(lead_id=received_lead.id, payment=payment)
                logger.info("Payment has been added to lead %s successfuly", received_lead.id)


@dataclass(frozen=True, eq=False)
class UpdateSubscriberToCrmUseCase:
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

        if not subscriber.source_id:
            logger.warning("Subscriber %s source id is not provided", subscriber.id)
            return

        received_client = self.keycrm_client.get_client_by_id(client_id=subscriber.source_id)

        if not received_client:
            logger.warning("There is no client by id: %s", subscriber.source_id)
            return

        logger.info("Clint %s has been received successfuly", received_client.id)

        received_client.full_name = " ".join(
            [value for value in [subscriber.first_name, subscriber.last_name] if value]
        )
        received_client.phone = None if received_client.phone == subscriber.phone else subscriber.phone
        received_client.username = None if received_client.username == subscriber.username else subscriber.username

        self.keycrm_client.update_client(client=received_client)
        logger.info("Clint %s has been updated successfuly", received_client.id)
