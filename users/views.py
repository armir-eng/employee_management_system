from django.shortcuts import render
from .models import *
from .serializers import *
from .permissions import *
from rest_framework import generics, response
from .querysets import *
from django_filters.rest_framework import DjangoFilterBackend
from permission_management.models import *
from employees.models import *
from departments.models import *
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your views here.


class UsersCreate(generics.CreateAPIView):

    queryset = Users.objects.all()
    serializer_class = UsersCreateSerializer
    permission_classes = [IsHR]

    def post(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['create_id'] = request.user.id
        request.data._mutable = _mutable

        return UsersCreate.create(self, request, *args, **kwargs)


class UsersList(generics.ListAPIView, UserQueryset):

    def get_queryset(self):

        user = self.request.user.users.all().values_list('role__role_name')

        if ('HR',) in list(user):
            return self.queryset

        if ('DM',) in list(user):
            a = super().user_queryset_department_manager()
            return a

        if ('DE',) in list(user):
            a = super().user_queryset_department_employee()
            return a

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['username', 'employee']
    permission_classes = [IsHR | IsDepartmentManager]


class UsersDetail(generics.RetrieveAPIView, UserQueryset):

    def get_queryset(self):

        user = self.request.user.users.all().values_list('role__role_name')

        if ('HR',) in list(user):
            return self.queryset

        if ('DM',) in list(user):
            a = super().user_queryset_department_manager()
            return a

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsHR | IsDepartmentManager | IsEmployee]


class UsersUpdate(generics.UpdateAPIView, UserQueryset):

    def get_queryset(self):

        user = self.request.user.users.all().values_list('role__role_name')

        if ('HR',) in list(user):
            return self.queryset

        if ('DM',) in list(user):
            a = super().user_queryset_department_manager()
            return a

        if ('DE',) in list(user):
            a = super().user_queryset_department_employee()
            return a

    queryset = Users.objects.all()
    serializer_class = UsersUpdateSerializer
    permission_classes = [IsHR | IsDepartmentManager | IsEmployee]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UsersDelete(generics.DestroyAPIView):

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsHR]

    def delete(self, request, *args, **kwargs):
        user = Users.objects.get(id=kwargs.get('pk'))
        if not user.is_active:
            return Response({'error_message': "Could not delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(UsersDelete, self).delete(request=request, *args, **kwargs)


class UserRoleCreate(generics.CreateAPIView):

    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsHR]

    def post(self, *args, **kwargs):
        return UserRoleCreate.create(self, *args, **kwargs)


class UserRoleDetail(generics.RetrieveAPIView, UserRoleQueryset):

    def get_queryset(self):

        user = self.request.user.users.all().values_list('role__role_name')

        if ('HR',) in list(user):
            return self.queryset

        if ('DM',) in list(user):
            a = super().user_role_queryset_department_manager
            return a

        if ('DE',) in list(user):
            a = super().user_role_queryset_department_employee
            return a

    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsHR | IsDepartmentManager | IsEmployee]


class UserRoleUpdate(generics.UpdateAPIView):

    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsHR]


class UserRoleDelete(generics.DestroyAPIView):

    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsHR]

    def delete(self, request, *args, **kwargs):
        user_role = UserRole.objects.get(id=kwargs.get('pk'))
        if not user_role.active:
            return Response({'error_message': "Could not delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(UserRoleDelete, self).delete(request=request, *args, **kwargs)


class UserRoleList(generics.ListAPIView, UserRoleQueryset):

    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

    def get_queryset(self):

        user = self.request.user.users.all().values_list('role__role_name')

        if ('HR',) in list(user):
            return self.queryset.all()

        if ('DM',) in list(user):
            a = super().user_role_queryset_department_manager
            return a

        if ('DE',) in list(user):
            a = super().user_role_queryset_department_employee
            return a


class RoleCreate(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsHR]

    def post(self, *args, **kwargs):
        return RoleCreate.create(self, *args, **kwargs)


class RoleDetail(generics.RetrieveAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleList(generics.RetrieveAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleUpdate(generics.UpdateAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsHR]


class RoleDelete(generics.DestroyAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsHR]

    def delete(self, request, *args, **kwargs):
        role = models.Role.objects.get(id=kwargs.get('pk'))
        if not role.active:
            return Response({'error_message': "Could not delete"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(RoleDelete, self).delete(request=request, *args, **kwargs)
