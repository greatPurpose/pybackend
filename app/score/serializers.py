from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Score
from user.serializers import UserSerializer


class GetScoreSerializer(UserSerializer):
    """Calculates score without requiring password or storing user"""

    class Meta(UserSerializer.Meta):
        extra_kwargs = {'password': {'read_only': True}}

    def calculate_score(self):
        user = get_user_model()(**self.data)
        return user.calculate_score()


class ScoreSerializer(serializers.ModelSerializer):
    """Serializer for score object"""

    class Meta:
        model = Score
        fields = (
            'id',
            'score_overall',
            'score_medical',
            'score_income',
            'score_stuff',
            'score_liability',
            'score_digital',
            'content_overall',
            'content_medical',
            'content_income',
            'content_stuff',
            'content_liability',
            'content_digital',
        )
        read_only_fields = ('id',)
