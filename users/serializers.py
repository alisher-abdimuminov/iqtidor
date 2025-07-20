from rest_framework import serializers

from .models import User, Group, Invite


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "teacher",
            "name",
            "count_members",
            "max_members",
            "created",
        )


class InvitesSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    class Meta:
        model = Invite
        fields = ("id", "group", )


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
        )


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "first_name",
            "last_name",
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
