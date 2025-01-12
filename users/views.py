from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from users.models import Payment


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ["payment_date", "paid_course", "paid_lesson", "payment_method"]
