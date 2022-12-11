from django.core.validators import FileExtensionValidator
from django.db import models

from characters.utils import upload_csv


class Collection(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    csv = models.FileField(
        validators=[FileExtensionValidator(["csv"])], upload_to=upload_csv
    )

    def __str__(self) -> str:
        return self.created_at.strftime("%b. %d. %Y %H.%M %P")

    @property
    def csv_clear_name(self):
        return self.csv.name.split("/")[-1]
