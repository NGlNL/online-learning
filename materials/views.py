from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, generics

from materials.models import Course, Lesson, Subscription
from materials.paginators import MyPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from users.permissions import IsModer, IsOwner

from .tasks import send_mail_about_course


class CourseViewSet(ModelViewSet):
    """ViewSet для работы с курсами."""

    queryset = Course.objects.all()
    pagination_class = MyPagination

    def get_serializer_class(self):
        """Возвращает класс сериализатора в зависимости от действия."""
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        """Возвращает список разрешений в зависимости от действия."""
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail_about_course.delay(instance.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonCreateAPIView(generics.CreateAPIView):
    """APIView для создания уроков."""

    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)
    pagination_class = MyPagination


class LessonLisAPIView(generics.ListAPIView):
    """APIView для получения списка уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """APIView для получения уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """APIView для обновления уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """APIView для удаления уроков."""

    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class SubscriptionView(APIView):
    """APIView для подписки на курс."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message}, status=status.HTTP_200_OK)
