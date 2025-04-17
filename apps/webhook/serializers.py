from rest_framework import serializers


class PaymentWebhookSerializer(serializers.Serializer):
    lead_id = serializers.IntegerField()
    amount = serializers.FloatField()
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=(("paid", "Paid"), ("closed", "Closed")))
    payment_date = serializers.DateTimeField()
    transaction_uuid = serializers.CharField()
