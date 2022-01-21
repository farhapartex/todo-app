from django.contrib.auth.models import User
from rest_framework import serializers, fields
from core.models import Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username")


class TaskListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "user", "name", "deadline", "status")


class TaskDetailsSerializer(serializers.ModelSerializer):
    deadline = fields.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])

    class Meta:
        model = Task
        fields = ("id", "user", "name", "description", "deadline", "status")
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        instance = Task.objects.create(**validated_data)
        return instance


class TaskUpdateSerializer(serializers.ModelSerializer):
    deadline = fields.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])

    class Meta:
        model = Task
        fields = ("id", "user", "name", "description", "deadline", "status")
        extra_kwargs = {
            'user': {'read_only': True},
        }