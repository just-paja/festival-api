from api.rest import accomodations, capacity, lector_roles, lectors, meals,\
    orders,\
    participants, payments, rules, schedule, teams, workshop_difficulties,\
    workshops, years
from api_textual.rest import news, performers, polls, texts, workshop_locations

from rest_framework import routers

from rest_framework_extensions.routers import NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass


router = NestedDefaultRouter()
router.register(r'lectorRoles', lector_roles.LectorRoleViewSet)
router.register(r'lectors', lectors.LectorViewSet)
router.register(r'news', news.NewsViewSet)
router.register(r'orders', orders.OrderViewSet)
router.register(r'payments', payments.PaymentViewSet)
router\
    .register(r'polls', polls.PollViewSet)\
    .register(
        r'vote',
        polls.PollVoteViewSet,
        base_name='poll-vote',
        parents_query_lookups=['answer__poll'],
    )
router.register(r'teams', teams.TeamsViewSet)
router.register(r'texts', texts.TextViewSet)
router.register(r'whoAmI', participants.WhoAmIViewSet)
router.register(
    r'workshopDifficulties',
    workshop_difficulties.WorkshopDifficultyViewSet,
)
router.register(r'years', years.YearViewSet)
router.register(r'register', participants.RegistrationViewSet)
router.register(
    r'years/(?P<year>[0-9]{4})/workshops',
    workshops.WorkshopViewSet,
    base_name='workshops',
).register(
    r'participants',
    participants.ParticipantViewSet,
    base_name='workshops-participants',
    parents_query_lookups=['assigned_workshop'],
)
router.register(
    r'years/(?P<year>[0-9]{4})/locations',
    workshop_locations.WorkshopLocationViewSet,
    base_name='locations',
)
router.register(
    r'years/(?P<year>[0-9]{4})/meals',
    meals.MealViewSet,
    base_name='meals',
)
router.register(
    r'years/(?P<year>[0-9]{4})/rules',
    rules.RulesViewSet,
    base_name='rules',
)
router.register(
    r'years/(?P<year>[0-9]{4})/performers',
    performers.PerformerViewSet,
    base_name='performers',
)
router.register(
    r'years/(?P<year>[0-9]{4})/schedule',
    schedule.ScheduleEventViewSet,
    base_name='schedule',
)
router.register(
    r'years/(?P<year>[0-9]{4})/capacity',
    capacity.CapacityViewSet,
    base_name='capacity',
)

router.register(r'accomodations', accomodations.AccomodationViewSet)
