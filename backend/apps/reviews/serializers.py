"""Serializers for reviews."""
from rest_framework import serializers
from .models import Review, ReviewImage


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image_url']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.CharField(source='user.profile_picture', read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'property', 'rating', 'comment',
            'is_approved', 'images', 'user_name', 'user_avatar',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'is_approved', 'created_at', 'updated_at']

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class ReviewCreateSerializer(serializers.ModelSerializer):
    image_urls = serializers.ListField(
        child=serializers.URLField(), required=False, write_only=True
    )

    class Meta:
        model = Review
        fields = ['property', 'rating', 'comment', 'image_urls']

    def create(self, validated_data):
        image_urls = validated_data.pop('image_urls', [])
        validated_data['user'] = self.context['request'].user
        review = super().create(validated_data)
        for url in image_urls:
            ReviewImage.objects.create(review=review, image_url=url)
        return review
