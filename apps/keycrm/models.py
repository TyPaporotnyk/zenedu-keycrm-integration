from django.db import models

from apps.common.models import TimedBaseModel
from apps.keycrm import entities


class Pipeline(TimedBaseModel):
    name = models.CharField(max_length=255)

    def to_entity(self) -> entities.Pipeline:
        return entities.Pipeline(id=self.id, name=self.name)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Pipeline"
        verbose_name_plural = "Pipelines"
        ordering = ["id"]


class Integration(TimedBaseModel):
    bot = models.ForeignKey("zenedu.Bot", on_delete=models.CASCADE)
    pipeline = models.ForeignKey("keycrm.Pipeline", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def to_entity(self) -> entities.Integration:
        return entities.Integration(
            id=self.id,
            bot_id=self.bot_id,
            pipeline_id=self.pipeline_id,
            is_active=self.is_active,
        )

    def __str__(self):
        return f"{self.bot} - {self.pipeline}"

    class Meta:
        verbose_name = "Zenedu integration"
        verbose_name_plural = "Zenedu integrations"
        unique_together = ["bot", "pipeline"]
