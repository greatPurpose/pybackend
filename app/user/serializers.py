from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = (
            'phone_number',
            'password',
            'email',
            'name',
            'first_name',
            'last_name',
            'age',
            'zipcode',
            'income',
            'savings',
            'debt',
            'education',
            'employment',
            'score',
            'own_vehicle',
            'own_pet',
            'own_rent_house',
            'have_health_cover',
            'have_dental_cover',
            'have_vision_cover',
            'have_life_cover',
            'have_longtermdisability_cover',
            'have_shorttermdisability_cover',
            'have_accident_cover',
            'have_criticalillness_cover',
            'have_auto_cover',
            'have_homeowner_cover',
            'have_renters_cover',
            'date_joined',
            'is_active',
            'is_staff',
        )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        score = user.calculate_score()
        score.save()
        user.score = score
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    phone_number = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = authenticate(
            requests=self.context.get('request'),
            username=phone_number,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
