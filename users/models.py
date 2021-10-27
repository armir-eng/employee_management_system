from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Users(AbstractUser):
      
      username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
      email = models.EmailField(_('email address'), unique = True)
      USERNAME_FIELD = 'email'
      REQUIRED_FIELDS = ['username']
      is_active = models.BooleanField(default=True)
      is_staff = models.BooleanField(default=True)  # a admin user; non super-user
      is_admin = models.BooleanField(default=False)
      is_superuser = models.BooleanField(default=False)
      
      def __str__(self):
            return f"{self.username}" 

class Role(models.Model):
      
      USER_ROLE=(('HR','Human Resources'), ('DM','Department Manager'), ('DE','Department Employee'),)
      role_name=models.CharField(max_length=30, choices=USER_ROLE, help_text='Role of a user in system')
      
      def __str__(self):
            return self.get_role_name_display()

class UserRole(models.Model):
    
    user=models.ForeignKey('Users', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='users')
    role=models.ForeignKey('Role', on_delete=models.DO_NOTHING, null=True, blank= True, help_text='Role of a user in system')
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.employee} - {self.role.role_name}"
