from django.db.models import CharField, ImageField, PositiveIntegerField, PositiveSmallIntegerField

from common.models import ActiveModel, TitledModel


class Offer(ActiveModel, TitledModel):
    feature = CharField(
        max_length=255,
    )
    logo = ImageField(upload_to="offer-logos")
    sum = PositiveIntegerField()
    days = PositiveSmallIntegerField()
    interestRate = CharField(
        max_length=255,
    )
    time = CharField(
        max_length=255,
    )
    offerId = PositiveIntegerField()

    my_order = PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ["my_order"]
        verbose_name = "Предложение МФО"
        verbose_name_plural = "Предложения МФО"

    def __str__(self):
        if not self.is_active:
            return f"!НЕАКТИВЕН! {self.title}"
        return self.title
