"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .lector import Lector
from .lectorRole import LectorRole


class WorkshopLector(Base):
    """Stores lector roless."""

    class Meta:
        verbose_name = _("Workshop lector")
        verbose_name_plural = _("Workshop lectors")

    lector = models.ForeignKey(
        Lector,
        verbose_name=_("Lector"),
    )
    workshop = models.ForeignKey(
        'Workshop',
        verbose_name=_("Workshop"),
    )
    role = models.ForeignKey(
        LectorRole,
        verbose_name=_("Lector role"),
    )

    def __str__(self):
        """Return name as string representation."""
        return "%s (%s)" % (self.lector, self.role)
