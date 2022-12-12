import uuid

from django.conf import settings


def upload_csv(instance: "Collection", file_name: str) -> str:
    return f"{settings.FILES_PATH}collections/{uuid.uuid4()}.csv"
