import logging
from dataclasses import dataclass

from apps.zenedu.clients import ZeneduClient
from apps.zenedu.services import BotService, SubscriberService

logger = logging.getLogger(__name__)


@dataclass
class LoadAllBotsUseCase:
    zenedu_client: ZeneduClient
    bot_service: BotService

    def execute(self):
        bots = self.zenedu_client.get_all_bots()
        logger.info("Received %s bots", len(bots))

        for bot in bots:
            _, is_created = self.bot_service.create_or_update(bot=bot)

            if is_created:
                logger.info("Bot %s has been created", bot.username)
            else:
                logger.info("Bot %s has been updated", bot.username)


@dataclass
class LoadAllSubscribersUseCase:
    zenedu_client: ZeneduClient
    bot_service: BotService
    subscriber_service: SubscriberService

    def execute(self):
        from apps.keycrm.tasks import create_subscriber_to_crm_task, update_subscriber_to_crm_task

        bots = self.bot_service.get_all_active_bots()
        logger.info("Selected %s active bots", len(bots))

        for bot in bots:
            if not bot.is_active:
                return

            subscribers = self.zenedu_client.get_all_customers_by_bot_id(bot_id=bot.id)
            logger.info("Received %s customer by bot id %s", len(subscribers), bot.id)

            for subscriber in subscribers:
                old_subscriber = self.subscriber_service.get_by_id(subscriber_id=subscriber.id)
                new_subscriber, is_created = self.subscriber_service.create_or_update(subscriber=subscriber)

                if is_created:
                    logger.info("Subscriber %s has been created successfuly", new_subscriber.id)
                    create_subscriber_to_crm_task.delay(subscriber_id=new_subscriber.id, bot_id=bot.id)
                elif new_subscriber != old_subscriber:
                    logger.info("Subscriber %s has been updated successfuly", new_subscriber.id)
                    update_subscriber_to_crm_task.delay(subscriber_id=new_subscriber.id, bot_id=bot.id)
