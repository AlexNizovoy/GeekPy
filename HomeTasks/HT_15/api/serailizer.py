from rest_framework import serializers

from stories.models import Story, StoryCategory, StoryType


class StoryCategorySerializer(serializers.ModelSerializer):
    stories = serializers.StringRelatedField(many=True)

    class Meta:
        model = StoryCategory
        fields = '__all__'


class StoryTypeSerializer(serializers.ModelSerializer):
    stories = serializers.StringRelatedField(many=True)

    class Meta:
        model = StoryType
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    story_type = serializers.StringRelatedField(many=False)
    story_category = serializers.StringRelatedField(many=False)

    class Meta:
        model = Story
        fields = '__all__'
