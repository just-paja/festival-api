from rest_framework import serializers

from .workshops import WorkshopPriceSerializer

from ..models import Food, Meal, MealReservation, Reservation, Soup


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            'name',
            'price',
            'date',
        )


class FoodSerializer(serializers.ModelSerializer):
    meal = MealSerializer(many=False, read_only=True)

    class Meta:
        model = Food
        fields = (
            'id',
            'name',
            'meal',
        )


class SoupSerializer(serializers.ModelSerializer):
    meal = MealSerializer(many=False, read_only=True)

    class Meta:
        model = Soup
        fields = (
            'id',
            'name',
            'meal',
        )


class MealReservationSerializer(serializers.ModelSerializer):
    food = FoodSerializer(many=False, read_only=True)
    soup = SoupSerializer(many=False, read_only=True)

    class Meta:
        model = MealReservation
        fields = (
            'id',
            'food',
            'soup',
        )


class ReservationSerializer(serializers.ModelSerializer):
    endsAt = serializers.DateTimeField(source='ends_at')
    mealReservation = MealReservationSerializer(
        source='meals',
        many=True,
        read_only=True,
    )
    workshopPrice = WorkshopPriceSerializer(
        source="workshop_price",
        many=False,
        read_only=True,
    )

    class Meta:
        model = Reservation
        fields = (
            'id',
            'endsAt',
            'mealReservation',
            'workshopPrice',
            'accomodation',
        )
