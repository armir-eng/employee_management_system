from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *

class UsersCreateSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField( 
           style={'input_type': 'password'},
           min_length=6, 
           max_length=68, 
           write_only=True)
    
    class Meta:
        model = Users
        fields=['email','username','password','is_staff','is_admin','is_superuser']
        
    
    def create(self, validated_data):
        user = Users(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user   
        
         
class UsersSerializer(serializers.ModelSerializer):
        class Meta:
            model = Users
            fields = '__all__'
        
class UsersUpdateSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField( 
           style={'input_type': 'password'},
           min_length=6, 
           max_length=68, 
           write_only=True)
    new_password = serializers.CharField( 
           style={'input_type': 'password'},
           min_length=6, 
           max_length=68, 
           write_only=True)    
    
    class Meta:
        model = Users
        fields=['email','username','first_name','last_name','is_active','is_staff','is_admin','is_superuser','confirm_password','new_password']

    def update(self, instance, validated_data):
        
        instance.email = validated_data.get('email', instance.email)
        instance.username= validated_data.get('username', instance.username)
        instance.first_name= validated_data.get('first_name', instance.first_name)
        instance.last_name= validated_data.get('last_name', instance.last_name)
        instance.is_active= validated_data.get('is_active', instance.is_active)
        instance.is_staff= validated_data.get('is_staff', instance.is_staff)
        instance.is_admin= validated_data.get('is_admin', instance.is_admin)
        instance.is_superuser= validated_data.get('is_superuser', instance.is_superuser)
        
        
        instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
              raise serializers.ValidationError({'new_password': 'not found'})

        
        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['confirm_password']: 
            # instance.password = validated_data['new_password'] 
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance
        
        return instance
        super(UsersUpdateSerializer,self).save(*args, **kwargs)  


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRole
        fields='__all__'


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'