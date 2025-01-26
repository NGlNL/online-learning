from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


def validate_link(value):
    parsed_link = urlparse(value)
    if parsed_link.netloc not in ["www.youtube.com", "youtube.com"]:
        raise ValidationError("Ссылка недопустима. Разрешены только ссылки на YouTube.")
