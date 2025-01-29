from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonLisAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView,
                             SubscriptionView)

app_name = "materials"

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/", LessonLisAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
] + router.urls
