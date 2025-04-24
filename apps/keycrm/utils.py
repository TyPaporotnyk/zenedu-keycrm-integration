from apps.zenedu.entities import Bot, Subscriber


def get_payment_description(subscriber: Subscriber, bot: Bot) -> str:
    return "Заказ с бота {bot}, клиент {subscriber}".format(bot=bot.name, subscriber=subscriber.full_name)
