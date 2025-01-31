from apps.zenedu import entities
from apps.zenedu.models import Bot, Subscriber


class BotService:

    def get_all_active_bots(self) -> list[entities.Bot]:
        bots = Bot.objects.filter(is_active=True)
        return [bot.to_entity() for bot in bots]

    def create_or_update(self, bot: entities.Bot) -> tuple[entities.Bot, bool]:
        defaults = {
            "name": bot.name,
            "username": bot.username,
            "is_active": bot.is_active,
        }
        obj, is_created = Bot.objects.update_or_create(
            id=bot.id,
            defaults=defaults,
            create_defaults={"created_at": bot.created_at, **defaults},
        )

        return obj.to_entity(), is_created


class SubscriberService:

    def get_by_id(self, subscriber_id: int) -> entities.Subscriber | None:
        try:
            obj = Subscriber.objects.get(pk=subscriber_id)

            return obj.to_entity()
        except Subscriber.DoesNotExist:
            return None

    def create_or_update(self, subscriber: entities.Subscriber) -> tuple[entities.Subscriber, bool]:
        defaults = {
            "first_name": subscriber.first_name,
            "last_name": subscriber.last_name,
            "username": subscriber.username,
            "phone": subscriber.phone,
        }
        obj, is_created = Subscriber.objects.update_or_create(
            id=subscriber.id,
            defaults=defaults,
            create_defaults={"created_at": subscriber.created_at, **defaults},
        )

        return obj.to_entity(), is_created

    def update(self, subscriber: entities.Subscriber) -> entities.Subscriber:
        defaults = {
            "first_name": subscriber.first_name,
            "last_name": subscriber.last_name,
            "username": subscriber.username,
            "phone": subscriber.phone,
            "source_id": subscriber.source_id,
        }

        obj = Subscriber.objects.get(pk=subscriber.id)
        for key, value in defaults.items():
            setattr(obj, key, value)
        obj.save()

        return obj.to_entity()

    def partial_update(self, subscriber_id: int, **fields) -> entities.Subscriber:
        obj = Subscriber.objects.get(pk=subscriber_id)
        for key, value in fields.items():
            setattr(obj, key, value)
        obj.save()

        return obj.to_entity()
