from django.urls import path

from . import views

urlpatterns = [path("payment/", views.WFPPaymentWebhook.as_view())]
