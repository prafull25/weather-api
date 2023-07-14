from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()
    output_format = serializers.ChoiceField(choices=["json", "xml"])


class WeatherResponseSerializer(serializers.Serializer):
    Weather = serializers.FloatField()
    Latitude = serializers.FloatField()
    Longitude = serializers.FloatField()
    City = serializers.CharField(max_length=255)
