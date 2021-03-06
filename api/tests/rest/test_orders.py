"""Tests for orders rest endpoint."""

import json

from django.test import TestCase
from django.urls import reverse

from freezegun import freeze_time

from model_mommy import mommy

from rest_framework.test import APIRequestFactory, force_authenticate

from api.rest.orders import OrderViewSet, OrdersFoodViewSet


class OrdersEndpointTest(TestCase):
    """Test accomodation methods."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.default_user = mommy.make('api.Participant')
        self.order = mommy.make(
            'api.Order',
            participant=self.default_user,
        )
        self.price_level = mommy.make('api.PriceLevel')
        self.workshop = mommy.make('api.Workshop')
        self.price = mommy.make(
            'api.WorkshopPrice',
            price_level=self.price_level,
            workshop=self.workshop,
        )
        self.reservation = mommy.make(
            'api.Reservation',
            order=self.order,
            workshop_price=self.price,
        )
        self.view = OrderViewSet.as_view(
            actions={
                'get': 'retrieve',
                'delete': 'destroy',
                'patch': 'update',
            },
        )

    def test_order_update_missing_order(self):
        request = self.factory.patch(
            reverse('order-detail', args=[356568]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=356568).render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['unknown-object']},
        )

    def test_order_update_missing_workshop(self):
        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': 335757}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk)
        self.assertEqual(response.status_code, 404)

    def test_order_update_not_owned_order(self):
        invalid_user = mommy.make('api.Participant')
        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=invalid_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['must-be-owner']},
        )

    def test_order_update_no_reservation(self):
        order = mommy.make(
            'api.Order',
            participant=self.default_user,
        )
        request = self.factory.patch(
            reverse('order-detail', args=[order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['make-reservation-first']},
        )

    def test_order_update_no_workshop_price(self):
        order = mommy.make(
            'api.Order',
            participant=self.default_user,
            reservation=mommy.make('api.Reservation'),
        )
        request = self.factory.patch(
            reverse('order-detail', args=[order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['make-reservation-first']},
        )

    def test_order_update_price_level_mismatch(self):
        order = mommy.make(
            'api.Order',
            participant=self.default_user,
        )
        mommy.make(
            'api.Reservation',
            order=order,
            workshop_price=mommy.make(
                'api.WorkshopPrice',
                price_level=mommy.make('api.PriceLevel'),
            ),
        )

        request = self.factory.patch(
            reverse('order-detail', args=[order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['no-matching-price-level']},
        )

    @freeze_time('2017-01-01T00:00:00Z')
    def test_order_update_assigned_full(self):
        workshop = mommy.make(
            'Workshop',
            capacity=1,
        )
        price = mommy.make(
            'api.WorkshopPrice',
            price_level=self.price_level,
            workshop=workshop,
        )
        mommy.make(
            'api.reservation',
            workshop_price=price,
            ends_at='2017-01-05T00:00:00Z',
            orders__paid=True,
        )
        self.default_user.assigned_workshop = self.workshop
        self.default_user.save()

        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['workshop-is-full']},
        )

    @freeze_time('2017-01-01T00:00:00Z')
    def test_order_update_reserved_full(self):
        workshop = mommy.make(
            'Workshop',
            capacity=1,
        )
        price = mommy.make(
            'api.WorkshopPrice',
            price_level=self.price_level,
            workshop=workshop,
        )
        mommy.make(
            'api.Reservation',
            workshop_price=price,
            ends_at='2017-01-05T00:00:00Z',
            orders__paid=False,
        )
        self.default_user.assigned_workshop = self.workshop
        self.default_user.save()

        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['workshop-is-full']},
        )

    def test_order_update_no_change(self):
        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': self.workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 204)

    def test_order_update_no_reassignment(self):
        workshop = mommy.make('Workshop')
        price = mommy.make(
            'api.WorkshopPrice',
            price_level=self.price_level,
            workshop=workshop,
        )

        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 204)
        self.order.reservation.refresh_from_db()
        self.assertEqual(self.order.reservation.workshop_price.pk, price.pk)
        self.assertEqual(self.default_user.assigned_workshop, None)

    def test_order_update_reassignment(self):
        workshop = mommy.make('Workshop')
        price = mommy.make(
            'api.WorkshopPrice',
            price_level=self.price_level,
            workshop=workshop,
        )
        self.default_user.assigned_workshop = self.workshop
        self.default_user.save()

        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'workshop': workshop.pk}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 204)
        self.order.reservation.refresh_from_db()
        self.default_user.refresh_from_db()
        self.assertEqual(self.order.reservation.workshop_price.pk, price.pk)
        self.assertEqual(self.default_user.assigned_workshop.pk, workshop.pk)


class OrdersFoodEndpointTest(TestCase):
    """Test accomodation methods."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.default_user = mommy.make('api.Participant')
        self.order = mommy.make(
            'api.Order',
            participant=self.default_user,
        )
        self.reservation = mommy.make(
            'api.Reservation',
            order=self.order,
        )

        self.meal1 = mommy.make('Meal')
        self.meal2 = mommy.make('Meal')

        self.food1 = mommy.make('Food', meal=self.meal1)
        self.food2 = mommy.make('Food', meal=self.meal2)
        self.soup1 = mommy.make('Soup', meal=self.meal1)
        self.soup2 = mommy.make('Soup', meal=self.meal2)

        mommy.make('MealReservation', meal=self.meal1, reservation=self.reservation)
        mommy.make('MealReservation', meal=self.meal2, reservation=self.reservation)

        self.view = OrdersFoodViewSet.as_view(
            actions={
                'patch': 'update',
            },
        )

    def test_order_update_missing_order(self):
        request = self.factory.patch(
            reverse('order-detail', args=[3335]),
            json.dumps({'food': []}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=None).render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['unknown-object']},
        )

    def test_order_update_missing_food(self):
        request = self.factory.patch(
            reverse('order-detail', args=[356568]),
            json.dumps({}),
            content_type='application/json',
        )
        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=356568).render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['unknown-object']},
        )

    def test_order_update_not_owned_order(self):
        invalid_user = mommy.make('api.Participant')
        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({'foods': []}),
            content_type='application/json',
        )
        force_authenticate(request, user=invalid_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json.loads(response.content.decode('utf-8')),
            {'errors': ['must-be-owner']},
        )

    def test_order_update_foods(self):

        request = self.factory.patch(
            reverse('order-detail', args=[self.order.pk]),
            json.dumps({
                'food': {
                    self.meal1.pk: {
                        'food': self.food1.pk,
                        'soup': self.soup1.pk,
                    },
                    self.meal2.pk: {
                        'food': self.food2.pk,
                        'soup': self.soup2.pk,
                    },
                },
            }),
            content_type='application/json',
        )

        force_authenticate(request, user=self.default_user)
        response = self.view(request, pk=self.order.pk).render()
        self.assertEqual(response.status_code, 204)
        self.order.reservation.refresh_from_db()
        meal_reservations = self.order.reservation.mealreservation_set.all()
        self.assertEqual(meal_reservations[0].food, self.food1)
        self.assertEqual(meal_reservations[0].soup, self.soup1)
        self.assertEqual(meal_reservations[1].food, self.food2)
        self.assertEqual(meal_reservations[1].soup, self.soup2)
