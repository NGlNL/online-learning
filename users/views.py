from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (
    create_checkout_session,
    create_price,
    create_product,
    save_payment,
)


class PaymentViewSet(ModelViewSet):
    """ViewSet для работы с платежами."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
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


def create(self, request, *args, **kwargs):
    """Создание платежа."""
    course_id = request.data.get("paid_course")
    lesson_id = request.data.get("paid_lesson")
    amount = request.data.get("amount")

    if not course_id or not amount:
        return Response(
            {"error": "Отсутствуют обязательные параметры"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        course = Course.objects.get(id=course_id)
    except ObjectDoesNotExist:
        return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

    lesson = Lesson.objects.get(id=lesson_id) if lesson_id else None

    product = create_product(course.id)
    if not product:
        return Response(
            {"error": "Не удалось создать продукт"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    price = create_price(product.id, amount)
    if not price:
        return Response(
            {"error": "Не удалось создать цену"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    session = create_checkout_session(price.id)
    if not session:
        return Response(
            {"error": "Не удалось создать сессию оформления заказа"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    save_payment(
        user=request.user,
        course=course,
        lesson=lesson,
        amount=amount,
        session_id=session.id,
    )

    return Response({"url": session.url}, status=status.HTTP_201_CREATED)
