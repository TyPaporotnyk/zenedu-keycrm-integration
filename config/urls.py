from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def is_superuser(user):
    return user.is_superuser


superuser_required = user_passes_test(is_superuser)
admin_required = login_required(login_url="/admin/login/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/webwook/", include("apps.webhook.urls")),
    path(
        "api/v1/",
        admin_required(superuser_required(SpectacularAPIView.as_view())),
        name="schema",
    ),
    path(
        "api/v1/docs/",
        admin_required(superuser_required(SpectacularSwaggerView.as_view(url_name="schema"))),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        admin_required(superuser_required(SpectacularRedocView.as_view(url_name="schema"))),
        name="redoc",
    ),
]
