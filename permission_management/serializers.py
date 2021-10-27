from rest_framework import serializers
from .models import  Leave, Holiday

class HolidaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Holiday
        fields = '__all__'


class LeaveCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leave
        exclude = ['status']
    
    def create(self, validated_data):
       
        return Leave.objects.create(**validated_data)        
  

class LeaveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Leave
        fields = '__all__'


class Leave_2_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Leave
        fields=['start','end','status','active','reason','employee']


