from rest_framework import serializers

from api.fields import ContentField, LanguageField, ChannelField
from channel.models import ChannelNode, Content, TreeChannel
from common.models import Language


class TreeChannelDetailSerializer(serializers.ModelSerializer):

    root = ChannelField(many=True)

    class Meta:
        model = TreeChannel
        fields = '__all__'


class ContentDetailSerializer(serializers.ModelSerializer):

    channel = ChannelField()

    class Meta:
        model = Content
        fields = '__all__'


class ChannelNodeDetailSerializer(serializers.ModelSerializer):

    contents = ContentField(many=True)
    language = LanguageField()
    parent = ChannelField()

    class Meta:
        model = ChannelNode
        fields = '__all__'


class LanguageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'
