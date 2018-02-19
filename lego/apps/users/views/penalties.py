from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from lego.apps.permissions.api.views import AllowedPermissionsMixin
from lego.apps.users.models import Penalty
from lego.apps.users.serializers.penalties import PenaltySerializer
from lego.apps.users.filters import PenaltyFilterSet


class PenaltyViewSet(
    AllowedPermissionsMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Penalty.objects.all()
    serializer_class = PenaltySerializer
    filter_class = PenaltyFilterSet
