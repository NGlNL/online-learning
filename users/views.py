from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import UserSerializer


class PaymentViewSet(ModelViewSet):
    """ViewSet для работы с платежами."""
    queryset = Payment.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ["payment_date", "paid_course", "paid_lesson", "payment_method"]


class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserList(ListAPIView):
    """Список пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDetail(RetrieveAPIView):
    """Детальная информация о пользователе."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserUpdate(UpdateAPIView):
    """Обновление информации о пользователе."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDelete(DestroyAPIView):
    """Удаление пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
