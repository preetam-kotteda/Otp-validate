from .models import UserModel
from rest_framework import serializers

class phone_serializer(serializers.Serializer):
    phone = serializers.IntegerField(blank = False)
