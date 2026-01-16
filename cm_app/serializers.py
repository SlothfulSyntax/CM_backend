from rest_framework.serializers import ModelSerializer
from .models import *
class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'

from rest_framework import serializers

class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)

class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = ['id', 'company_name', 'image', 'description', 'apply_link', 'position', 'experience']

class ParticularJobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = '__all__'