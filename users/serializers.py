from rest_framework import serializers

from .models import User, Group, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "type",
            "tid",
            "service",
            "description",
            "state",
            "amount",
            "created",
        )


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "image",
        )


class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Group
        fields = (
            "id",
            "teacher",
            "name",
            "count_members",
            "created",
        )


class UserSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField("get_group")

    def get_group(self, obj: User):
        group = Group.objects.filter(members=obj)

        if not group.exists():
            return None

        group = group.first()

        return GroupSerializer(group).data

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "first_name",
            "last_name",
            "city",
            "town",
            "village",
            "school",
            "role",
            "group",
            "balance",
            "image",
        )


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "city",
            "town",
            "village",
            "school",
            "image",
        )


class SignUpBodySerializer(serializers.Serializer):
    phone = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    city = serializers.CharField()
    town = serializers.CharField()
    village = serializers.CharField()
    school = serializers.CharField()
    password = serializers.CharField()


class LoginBodySerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()


class EditProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    city = serializers.CharField()
    town = serializers.CharField()
    village = serializers.CharField()
    school = serializers.CharField()
