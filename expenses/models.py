from django.db import models
from django.conf import settings


class Expense(models.Model):
    """Expense model.

    Note: `user` is nullable to avoid NOT NULL constraint failures when adding the
    field to an existing table; you can make it required later after backfilling.
    """

    CATEGORY_CHOICES = [
        ('FOOD', 'FOOD'),
        ('TRAVEL', 'TRAVEL'),
        ('RENT', 'RENT'),
        ('SHOPPING', 'SHOPPING'),
        ('BILLS', 'BILLS'),
        ('OTHER', 'OTHER'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"