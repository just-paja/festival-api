"""Tests for workshop model."""

from django.test import TestCase
from freezegun import freeze_time
from model_mommy import mommy

from api.models import Workshop


class WorkshopTest(TestCase):
    """Test workshop methods."""

    def test_string_representation(self):
        """Test that workshop turns to string properly."""
        entry = Workshop(name="Foo Workshop")
        self.assertEqual(str(entry), 'Foo Workshop')

    @freeze_time("2017-02-01T00:00:00Z")
    def test_capacity(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at='2017-03-01T00:00:00Z',
            workshop_price__workshop__capacity=1,
        )
        reservation.order.save()
        workshop = reservation.workshop_price.workshop
        self.assertEqual(workshop.number_of_reservations(), 0)
        self.assertEqual(workshop.has_free_capacity(), False)

    @freeze_time("2017-02-01T00:00:00Z")
    def test_capacity_after_reservation(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at='2017-01-01T00:00:00Z',
            workshop_price__workshop__capacity=1,
            order__paid=False,
        )
        workshop = reservation.workshop_price.workshop
        self.assertEqual(workshop.number_of_reservations(), 0)
        self.assertEqual(workshop.has_free_capacity(), True)

    @freeze_time('2017-02-01T00:00:00Z')
    def test_capacity_assigned(self):
        workshop = mommy.make('api.Workshop', capacity=1)
        mommy.make(
            'api.ParticipantWorkshop',
            workshop=workshop,
        )
        self.assertEqual(workshop.number_of_reservations(), 1)
        self.assertEqual(workshop.has_free_capacity(), False)

    def test_lector_names(self):
        """ Test, that Workshop.lector_names() works correctly with one lector """
        workshop = mommy.make(
            'api.Workshop',
            lectors=[
                mommy.make('api.Lector', name="Foo lector"),
            ],
        )
        self.assertEqual(workshop.lector_names(), "Foo lector")

    def test_lector_names_two(self):
        """ Test, that Workshop.lector_names() works correctly with two lectors """
        workshop = mommy.make(
            'api.Workshop',
            lectors=[
                mommy.make('api.Lector', name="Foo lector"),
                mommy.make('api.Lector', name="Bar lector"),
            ],
        )
        self.assertEqual(workshop.lector_names(), "Foo lector, Bar lector")
