from rest_framework import permissions, serializers, viewsets

from .reservations import ReservationSerializer

from ..models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    reservation = ReservationSerializer(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            'id',
            # 'participant',
            'symvar',
            'price',
            'paid',
            'canceled',
            'reservation',
        )


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.participant:
            return Order.objects\
                .filter(participant=user.participant)\
                .prefetch_related('reservation')
