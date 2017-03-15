"""Base model class."""
import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class CapacityMixin(models.Model):
    """Mixin, that adds a capacity field and ensures that capacity is not exceeded"""

    capacity = models.PositiveIntegerField(
        verbose_name=_("Capacity"),
        help_text=_("How many people can fit in"),
        blank=True,
        null=True,
    )

    def get_reservations_query(self):
        """
        Returns query with reservations associated to self.
        """
        return NotImplemented

    def number_of_unpaid_reservations(self):
        """
        Returns number of participants who reserved this object, but doesn't paid.
        """
        from .participant import Participant
        return Participant.objects.filter(
            orders__canceled=False,
            orders__reservation__ends_at__gt=datetime.datetime.now(),
            orders__reservation__in=self.get_reservations_query(),
        ).exclude(
            orders__paid=True,
        ).distinct().count()

    def number_of_reservations(self):
        """
        Returns number of participants who reserved this object.
        """
        from .participant import Participant
        return Participant.objects.filter(
            Q(orders__paid=True) &
            Q(orders__reservation__in=self.get_reservations_query()),
        ).distinct().count()

    def has_free_capacity(self):
        """ Returns if the object has still a free capacity and other reservations can be add. """
        if self.capacity:
            total = self.number_of_unpaid_reservations() + \
                self.number_of_reservations()
            return total < self.capacity
        return True

    def available_capacity(self):
        """
        Returns number of avaliable places
        """
        return self.capacity - self.number_of_reservations()

    class Meta:
        """Makes the model abstract."""

        abstract = True
