import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import decorators, status
from rest_framework.response import Response

from apps.keycrm.clients import KeyCRMClient
from apps.keycrm.entities import Payment
from apps.webhook.serializers import PaymentWebhookSerializer
from config.containers import get_container

logger = logging.getLogger(__name__)


@extend_schema_view(post=extend_schema(request=PaymentWebhookSerializer))
class WFPPaymentWebhook(decorators.APIView):

    def post(self, *args, **kwargs):
        serializer = PaymentWebhookSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        container = get_container()
        client: KeyCRMClient = container.resolve(KeyCRMClient)

        payment = Payment(
            amount=serializer.validated_data["amount"],
            description=serializer.validated_data["description"],
            status=serializer.validated_data["status"],
            payment_date=serializer.validated_data["payment_date"],
            transaction_uuid=serializer.validated_data["transaction_uuid"],
        )

        try:
            client.add_payment_to_lead(lead_id=serializer.validated_data["lead_id"], payment=payment)
        except Exception as e:
            logger.warning(
                "Some error occured while adding transaction %s to lead %s: %s",
                serializer.validated_data["transaction_uuid"],
                serializer.validated_data["lead_id"],
                repr(e),
            )
        else:
            logger.info(
                "Transaction %s hass been added to lead %s successfuly",
                serializer.validated_data["transaction_uuid"],
                serializer.validated_data["lead_id"],
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
