from django.db.models import CharField, Model

from autoslug.fields import AutoSlugField


class TitledModel(Model):
    title = CharField(max_length=200, verbose_name="Название")
    slug = AutoSlugField(
        populate_from="title",
        db_index=True,
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
