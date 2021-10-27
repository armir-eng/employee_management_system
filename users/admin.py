from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(UserRole)
admin.site.register(Users,UserAdmin)
admin.site.register(Role)