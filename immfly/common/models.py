from django.db import models


class Language(models.Model):
    """
    Language stores all the available languages in
    ISO 631-9 code.
    """

    code = models.CharField(max_length=2, primary_key=True, unique=True)
    name = models.TextField(max_length=150, unique=True)

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super().save(*args, **kwargs)
