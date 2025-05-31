from django.db import models


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Table #{self.number}"
