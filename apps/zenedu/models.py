from django.db import models

from apps.common.models import TimedBaseModel
from apps.zenedu import entities


class Bot(TimedBaseModel):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField()

    def to_entity(self) -> entities.Bot:
        return entities.Bot(
            id=self.id,
            name=self.name,
            username=self.username,
            is_active=self.is_active,
            created_at=self.created_at,
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bot"
        verbose_name_plural = "Bots"
        ordering = ["-created_at"]


class Subscriber(TimedBaseModel):
    source_id = models.PositiveIntegerField(null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()

    def to_entity(self) -> entities.Subscriber:
        return entities.Subscriber(
            id=self.id,
            source_id=self.source_id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            phone=self.phone,
            created_at=self.created_at,
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.username}"

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"
        ordering = ["-created_at"]
