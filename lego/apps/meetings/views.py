from rest_framework import decorators, status, viewsets
from rest_framework.response import Response

from lego.apps.meetings.models import Meeting, MeetingInvitation
from lego.apps.meetings.permissions import MeetingInvitationPermissions, MeetingPermissions
from lego.apps.meetings.serializers import (MeetingGroupInvite, MeetingInvitationSerializer,
                                            MeetingInvitationUpdateSerializer, MeetingSerializer,
                                            MeetingUserInvite)


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.prefetch_related('invitations', 'invitations__user')
    permission_classes = (MeetingPermissions,)
    serializer_class = MeetingSerializer

    @decorators.detail_route(methods=['POST'], serializer_class=MeetingUserInvite)
    def invite_user(self, request, *args, **kwargs):
        meeting = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        meeting.invite_user(user)
        return Response(data='Invited user ' + str(user.id), status=status.HTTP_201_CREATED)

    @decorators.detail_route(methods=['POST'], serializer_class=MeetingGroupInvite)
    def invite_group(self, request, *args, **kwargs):
        meeting = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.validated_data['group']
        meeting.invite_group(group)
        return Response(data='Invited group ' + str(group.id), status=status.HTTP_201_CREATED)


class MeetingInvitationViewSet(viewsets.ModelViewSet):
    queryset = MeetingInvitation.objects.select_related('user')
    permission_classes = (MeetingInvitationPermissions,)
    lookup_field = 'user__id'

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return MeetingInvitationUpdateSerializer
        return MeetingInvitationSerializer

    def get_queryset(self):
        return MeetingInvitation.objects.filter(meeting=self.kwargs['meeting_pk'])