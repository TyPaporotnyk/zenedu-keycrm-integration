from django.contrib import admin

from apps.keycrm.models import Integration, Pipeline


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = (
        "bot",
        "pipeline",
        "is_active",
    )
    search_fields = ("bot", "pipeline")
    list_filter = ("is_active",)
