from rest_framework import serializers
from .models import URL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re

"""A seriazlizer to validate url format"""
class URLShortenSerializer(serializers.Serializer):
    original_url = serializers.CharField(required=True)

    def validate_original_url(self, value):
        """check if url start with protocol"""
        if not value.startswith(('http://', 'https://')):
            value = 'https://' + value

        url_pattern = re.compile(
            r'^(https?://)?' 
            r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6})' 
            r'(:\d+)?(/.*)?$' 
        )
        if not url_pattern.match(value):
            raise serializers.ValidationError("Enter a valid URL.")

        """check www to be treated same as without them"""
        domain = value.split('://')[1]
        if not domain.startswith('www.') and '.' in domain:
            value = value.replace('://', '://www.', 1)

        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid URL.")

        return value
""""A serializer to check url shortener sent"""
class URLRetrieveSerializer(serializers.Serializer):
    shortened_url = serializers.CharField(required=True, min_length=6, max_length=6)
