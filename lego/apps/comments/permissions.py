from lego.apps.permissions.models import ObjectPermissionsModel
from lego.apps.permissions.permissions import AbakusPermission
from lego.utils.content_types import VALIDATION_EXCEPTIONS, string_to_instance


class CommentPermission(AbakusPermission):

    def has_permission(self, request, view):

        has_permission = super(CommentPermission, self).has_permission(request, view)

        if not has_permission:
            return False

        if view.action == 'create':
            return self.check_target_permissions(request)

        return True

    def check_target_permissions(self, request):
        comment_target = None
        try:
            if request.data.get('comment_target') is not None:
                comment_target = string_to_instance(request.data.get('comment_target'))

        except VALIDATION_EXCEPTIONS:
            # Comment_target was not found. This will be raised in serializer at a later point.
            # Validation does not belong in permissions
            pass

        if comment_target:
            if isinstance(comment_target, ObjectPermissionsModel) \
                    and not comment_target.can_view(request.user):
                return False

        return True