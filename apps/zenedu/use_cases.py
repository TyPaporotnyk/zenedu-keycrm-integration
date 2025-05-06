import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from apps.wayforpay.client import WayForPayClient
from apps.wayforpay.entities import Transaction
from apps.zenedu.clients import ZeneduClient
from apps.zenedu.entities import Bot, Order, Subscriber
from apps.zenedu.services import BotService, OrderService, SubscriberService

logger = logging.getLogger(__name__)
DATE_BEGIN_INDEX = 5


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
    order_service: OrderService
    way_for_pay_client: WayForPayClient

    def execute(self):
        bots = self.bot_service.get_all_active_bots()
        transactions = self.way_for_pay_client.get_transaction_list(
            date_begin=datetime.now() - timedelta(days=DATE_BEGIN_INDEX), date_end=datetime.now()
        )
        logger.info("Selected %s active bots", len(bots))

        for bot in bots:
            if not bot.is_active:
                return

            subscribers = self.zenedu_client.get_subscribers_by_bot_id(bot_id=bot.id, per_page=100)
            orders = self.zenedu_client.get_orders_by_bot_id(bot_id=bot.id, per_page=100)

            logger.info("Received %s customer by bot id %s", len(subscribers), bot.id)

            for subscriber in subscribers:
                old_subscriber = self.subscriber_service.get_by_id(subscriber_id=subscriber.id)
                new_subscriber, is_created = self.subscriber_service.create_or_update(subscriber=subscriber)

                if is_created:
                    self._create_new_subscriber(
                        subscriber=new_subscriber, bot=bot, orders=orders, transactions=transactions
                    )
                elif new_subscriber != old_subscriber:
                    self._update_old_subscriber(subscriber_id=new_subscriber.id, bot_id=bot.id)

    def _create_new_subscriber(
        self, subscriber: Subscriber, bot: Bot, orders: list[Order], transactions: list[Transaction]
    ):
        from apps.keycrm.tasks import create_subscriber_to_crm_task

        subscriber_order = None
        for order in orders:
            if order.subscriber.id == subscriber.id:
                order.bot = bot

                created_order, _ = self.order_service.create_or_update(order=order)
                subscriber_order = created_order
                logger.info("Found order %s for new subscriber %s", order.source_id, subscriber.id)
                break

        subscriber_transaction: Transaction = (
            next((tramsaction for tramsaction in transactions if tramsaction.phone == subscriber.phone), None)
            if subscriber_order
            else None
        )

        if subscriber_transaction:
            self.subscriber_service.partial_update(subscriber_id=subscriber.id, email=subscriber_transaction.email)

        logger.info("Subscriber %s has been created successfuly", subscriber.id)
        create_subscriber_to_crm_task.delay(
            subscriber_id=subscriber.id, bot_id=bot.id, order_id=subscriber_order.id if subscriber_order else None
        )

    def _update_old_subscriber(self, subscriber: Subscriber, bot: Bot):
        from apps.keycrm.tasks import update_subscriber_to_crm_task

        logger.info("Subscriber %s has been updated successfuly", subscriber.id)
        update_subscriber_to_crm_task.delay(subscriber_id=subscriber.id, bot_id=bot.id)
