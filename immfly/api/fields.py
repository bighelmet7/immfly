from rest_framework import serializers


class ChannelField(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=250)


class ContentField(serializers.Serializer):

    meta_info = serializers.JSONField()
    rating_value = serializers.DecimalField(max_digits=4, decimal_places=2)


class LanguageField(serializers.Serializer):

    code = serializers.CharField(max_length=2)
    name = serializers.CharField(max_length=50)

