from rest_framework.permissions import BasePermission
from django.utils.translation import ugettext_lazy as _
from users.models import *
import logging

logger = logging.getLogger(__name__)
error_message = _("Improper Login. Attempted to log in as Anonymous User.")

class IsHR(BasePermission):
    message='NOT ALLOWED TO ACCESS THIS VIEW!'
    def has_permission(self, request, view):
        try:
            user_role = UserRole.objects.filter(user=request.user, role__role_name='HR')
            return any([user_role.active for user_role in user_role])
        except Exception as e:
            logger.exception(e)
            logger.debug(error_message, exc_info=True)


class IsDepartmentManager(BasePermission):

    def has_permission(self, request, view):
        try:
            user_role = UserRole.objects.filter(user=request.user, role__role_name='DM')
            return any([user_role.active for user_role in user_role])
        except Exception as e:
            logger.exception(e)
            logger.debug(error_message, exc_info=True)


class IsEmployee(BasePermission):

    def has_permission(self, request, view):
        try:
            user_role = UserRole.objects.filter(user=request.user, role__role_name='DE')
            return any([user_role.active for user_role in user_role])
        except Exception as e:
            logger.exception(e)
            logger.debug(error_message, exc_info=True)