from rest_framework import serializers
from .models import AddUser


#  Serializer for the adduser model. The fields used are username, email, job, age.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddUser
        fields = ('username', 'email', 'job', 'age')
