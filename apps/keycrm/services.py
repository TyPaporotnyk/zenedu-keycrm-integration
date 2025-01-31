from apps.keycrm import entities
from apps.keycrm.models import Integration, Pipeline


class PipelineService:

    def create_or_update(self, pipeline: entities.Pipeline) -> tuple[entities.Pipeline, bool]:
        defaults = {
            "name": pipeline.name,
        }
        obj, is_created = Pipeline.objects.update_or_create(
            id=pipeline.id,
            defaults=defaults,
            create_defaults=defaults,
        )

        return obj.to_entity(), is_created


class IntegrationService:

    def get_by_bot_id(self, bot_id: int) -> entities.Integration:
        try:
            obj = Integration.objects.get(bot_id=bot_id)

            return obj.to_entity()
        except Integration.DoesNotExist:
            return None
