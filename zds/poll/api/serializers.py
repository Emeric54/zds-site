from rest_framework import serializers

from zds.member.api.serializers import UserListSerializer
from zds.poll.models import Poll, Choice


class ChoiceSerializer(serializers.ModelSerializer):

    votes = serializers.IntegerField(source='get_count_votes')

    class Meta:
        model = Choice
        fields = ('pk', 'choice', 'votes')


class PollDetailSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('pk', 'title', 'anonymous_vote', 'type_vote', 'enddate', 'choices')


class UsersSerializers(serializers.ModelSerializer):

    users = UserListSerializer(source='get_users', many=True, read_only=True)

    class Meta:
        model = Choice
        fields = ('users',)