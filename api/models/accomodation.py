"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .capacityMixin import CapacityMixin
from .reservation import Reservation
from ..fields import VISIBILITY_CHOICES, VISIBILITY_PUBLIC


class Accomodation(CapacityMixin, Base):
    """Stores accomodation types."""

    name = models.CharField(
        verbose_name=_("Accomodation name"),
        help_text=_("eg. Hotel Stadion"),
        max_length=127,
    )
    address = models.CharField(
        blank=True,
        help_text=_("Full physical address of the accomodation"),
        max_length=255,
        null=True,
        verbose_name=_("Accomodation address"),
    )
    desc = models.TextField(
        verbose_name=_("Description formatted in Markdown"),
        help_text=_("eg. Describe room, location, type of accomodation"),
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Price"),
        help_text=_("Price per night in CZK"),
    )
    visibility = models.PositiveIntegerField(
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_PUBLIC,
    )
    capacity = models.PositiveIntegerField(
        default=12,
        verbose_name=_("Capacity"),
        help_text=_("How many people can fit in"),
    )
    requires_identification = models.BooleanField(
        default=False,
        verbose_name=_("Requires Identification"),
        help_text=_("This accomodation requires to know persons home address and ID number"),
    )
    year = models.ForeignKey(
        'Year',
        null=True,
        on_delete=models.PROTECT,
    )

    def get_reservations_query(self):
        """
        Returns query path from reservation to self.
        """
        return Reservation.objects.filter(accomodation=self)

    def __str__(self):
        """Return name as string representation."""
        if self.year:
            return "(%s) %s" % (self.year.year, self.name)
        return self.name
