"""Schedule event model."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .workshop import Workshop
from .year import Year


class ScheduleEvent(Base):
    """Stores events for years schedule."""

    year = models.ForeignKey(
        Year,
        verbose_name=_("Year"),
        related_name="events",
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    location_name = models.CharField(
        verbose_name=_("Location Name"),
        max_length=255,
        null=True,
        blank=True,
    )
    start_at = models.DateTimeField(
        verbose_name=_("Event start time"),
    )
    end_at = models.DateTimeField(
        verbose_name=_("Event end time"),
        blank=True,
        null=True,
    )
    workshops = models.ManyToManyField(
        Workshop,
        blank=True,
    )
    performer = models.ForeignKey(
        'api_textual.Performer',
        related_name='events',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        """Return name as string representation."""
        return "(%s) %s" % (self.year.year, self.name) if self.year else self.name
