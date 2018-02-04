"""Tests for meal model."""

from django.test import TestCase
from freezegun import freeze_time
from model_mommy import mommy

from api.models import Meal


class MealTest(TestCase):
    """Test Meal methods."""

    def test_string_representation(self):
        """Test that meal turns to string properly."""
        entry = Meal(
            name="Foo Meal",
            date="2017-02-01",
        )
        self.assertEqual(str(entry), 'Foo Meal at 2017-02-01')

    @freeze_time("2017-02-01")
    def test_capacity(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at='2017-03-01T00:00:00Z',
            meal__capacity=1,
            reservation__order__paid=True,
        )
        meal_reservation.reservation.order.paid = True
        meal_reservation.reservation.order.save()
        meal = meal_reservation.meal
        self.assertEqual(meal.number_of_reservations(), 1)
        self.assertEqual(meal.has_free_capacity(), False)

    @freeze_time("2017-02-01")
    def test_capacity_after_reservation(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at='2017-01-01T00:00:00Z',
            meal__capacity=1,
            reservation__order__paid=False,
        )
        meal = meal_reservation.meal
        self.assertEqual(meal.number_of_reservations(), 0)
        self.assertEqual(meal.has_free_capacity(), True)

    @freeze_time("2017-02-01")
    def test_capacity_paid(self):
        meal_reservation = mommy.make(
            'api.MealReservation',
            reservation__ends_at='2017-01-01T00:00:00Z',
            meal__capacity=1,
            reservation__order__paid=True,
            reservation__order__participant__name="Foo participant",
        )
        meal_reservation.reservation.order.paid = True
        meal_reservation.reservation.order.save()
        meal = meal_reservation.meal
        self.assertEqual(meal.number_of_reservations(), 1)
        self.assertEqual(meal.has_free_capacity(), False)
