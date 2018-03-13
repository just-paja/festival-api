from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.db.utils import DatabaseError
from django.shortcuts import get_object_or_404

from rest_framework import permissions, response, serializers, status, viewsets

from .payments import PaymentSerializer
from .reservations import ReservationSerializer

from ..models import Food, Meal, MealReservation, Order, Reservation, Soup,\
    Workshop, Year


class OrderSerializer(serializers.ModelSerializer):
    accomodationInfo = serializers.BooleanField(source='accomodation_info')
    cancelled = serializers.BooleanField(source='canceled')
    createdAt = serializers.DateTimeField(source='created_at')
    reservation = ReservationSerializer(
        many=False,
        read_only=True,
    )
    payments = PaymentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            'accomodationInfo',
            'cancelled',
            'confirmed',
            'createdAt',
            'id',
            'paid',
            'participant',
            'payments',
            'price',
            'reservation',
            'symvar',
            'year',
        )


class CreateOrderSerializer(serializers.Serializer):
    workshop = serializers.IntegerField(required=False, allow_null=True, default=None)
    meals = serializers.ListField()
    accomodation = serializers.IntegerField()
    accomodationInfo = serializers.BooleanField(required=False)

    def create(self, validated_data):
        try:
            year = Year.objects.filter(current=True).order_by('-year').first()
        except ObjectDoesNotExist:
            year = None

        if not year:
            return None

        total_price = 0
        if 'workshop' in validated_data and validated_data['workshop']:
            workshop = Workshop.objects.get(id=validated_data['workshop'])
            workshop_price = workshop.get_actual_workshop_price(year)
            total_price += workshop_price.price
        else:
            workshop = None
            workshop_price = None

        meals = Meal.objects.filter(id__in=validated_data['meals'])
        meals_price = meals.aggregate(Sum('price'))['price__sum']

        if meals_price:
            total_price += meals_price

        order = Order.objects.create(
            participant=self.user.participant,
            price=total_price,
            accomodation_info=validated_data.get('accomodationInfo', False),
            year=year,
        )
        reservation = Reservation.objects.create(
            accomodation_id=validated_data['accomodation'],
            workshop_price=workshop_price,
            order=order,
        )
        for meal in meals:
            MealReservation.objects.create(
                meal=meal,
                reservation=reservation,
            )
        reservation.update_price()
        return order

    def update(self, instance, validated_data):
        return super().update()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.participant:
            return Order.objects\
                .filter(participant=user.participant)\
                .prefetch_related('reservation')\
                .prefetch_related('payments')

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        if order.participant != request.user.participant:
            return response.Response(
                "Requested object doesn't belong to authentificated user",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if 'confirm' in request.GET:
            order.confirm()
            order.refresh_from_db()
        return super().retrieve(request, *args, **kwargs)

    def create(self, request):
        try:
            year = Year.objects.filter(current=True).order_by('-year').first()
        except ObjectDoesNotExist:
            year = None
        serializer = CreateOrderSerializer(data=request.data)
        serializer.user = request.user.participant
        if year and serializer.user.participant and serializer.is_valid():
            openOrders = Order.objects.filter(
                canceled=False,
                participant=request.user.participant,
                year=year,
            ).count()
            if openOrders == 0:
                serializer.save()
                return response.Response(
                    OrderSerializer(
                        instance=serializer.instance,
                        context={'request': request},
                    ).data,
                )
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None, *args, **kwargs):
        order = Order.objects.filter(pk=pk).first()
        next_workshop = Workshop.objects\
            .filter(pk=request.data.get('workshop', None))\
            .first()

        if not order or not next_workshop:
            return response.Response(
                {'errors': ['unknown-object']},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.participant != request.user.participant:
            return response.Response(
                {'errors': ['must-be-owner']},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            reservation = order.reservation
        except ObjectDoesNotExist:
            reservation = None

        # get current order reservation or 404
        if not reservation or not reservation.workshop_price:
            return response.Response(
                {'errors': ['make-reservation-first']},
                status=status.HTTP_403_FORBIDDEN,
            )

        current_price_level = reservation.workshop_price.price_level
        current_workshop = reservation.workshop_price.workshop
        next_price = next_workshop.prices.filter(
            price_level=current_price_level,
        ).first()

        if not next_price:
            return response.Response(
                {'errors': ['no-matching-price-level']},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not next_workshop.has_free_capacity():
            return response.Response(
                {'errors': ['workshop-is-full']},
                status=status.HTTP_403_FORBIDDEN,
            )

        reservation.workshop_price = next_price
        reservation.save()

        participant = self.request.user.participant
        if participant.assigned_workshop == current_workshop:
            participant.assigned_workshop = next_workshop
            participant.save()

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        if order.participant == request.user.participant and not order.paid:
            order.canceled = True
            order.save()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {
                "messages": ["cannot-cancel"],
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def save_food_changes(meals, foods, soups):
    foods = [Food.objects.get(pk=food) for food in foods]
    soups = [Soup.objects.get(pk=soup) for soup in soups]

    for meal_reservation in meals:
        for food in foods:
            print(food.meal.pk, meal_reservation.meal.pk)
            if food.meal.pk == meal_reservation.meal.pk:
                meal_reservation.food = food
        for soup in soups:
            if soup.meal.pk == meal_reservation.meal.pk:
                meal_reservation.soup = soup
        meal_reservation.save()


class OrdersFoodViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.none()
    permission_classes = [permissions.IsAuthenticated]
    serializer = OrderSerializer

    def get_queryset(self):
        return Order.objects\
            .filter(participant=self.request.user.participant)\
            .prefetch_related('reservation')

    def update(self, request, pk=None, *args, **kwargs):
        order = Order.objects.filter(pk=pk).first()

        if not order:
            return response.Response(
                {'errors': ['unknown-object']},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.participant != request.user.participant:
            return response.Response(
                {'errors': ['must-be-owner']},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            reservation = order.reservation
        except ObjectDoesNotExist:
            return response.Response(
                {
                    'messages': ['make-reservation-first'],
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            save_food_changes(
                reservation.mealreservation_set.all(),
                request.data.get('foods'),
                request.data.get('soups'),
            )
        except DatabaseError:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        return response.Response(status=status.HTTP_204_NO_CONTENT)
