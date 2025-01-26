from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class UserSerializer(ModelSerializer):
    """Сериализатор для модели пользователя"""
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.
    Позволяет преобразовывать данные о платежах в JSON и обратно.
    """
    class Meta:
        model = Payment
        fields = "__all__"
