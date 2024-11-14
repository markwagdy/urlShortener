from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from .models import URL
from django.core.cache import cache
from .task import increment_click_count
from .response_functions import success, notfound
from .serializer import URLShortenSerializer, URLRetrieveSerializer

CACHE_TIMEOUT = 60 * 60

@api_view(['POST'])
def shorten_url(request):
    serializer = URLShortenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    original_url = serializer.validated_data['original_url']
    shortened_url = get_random_string(6)

    url, created = URL.objects.get_or_create(
        original_url=original_url,
        defaults={'shortened_url': shortened_url}
    )
    
    if not created:
        shortened_url = url.shortened_url
    
    cache.set(shortened_url, original_url, timeout=CACHE_TIMEOUT)
    
    return success({"shortened_url": shortened_url})


@api_view(['GET'])
def get_original_url(request, shortened_url):
    original_url = cache.get(shortened_url)
    
    if not original_url:
        serializer = URLRetrieveSerializer(data={"shortened_url": shortened_url})
        serializer.is_valid(raise_exception=True)

        try:
            url = URL.objects.get(shortened_url=shortened_url)
            original_url = url.original_url
            cache.set(shortened_url, original_url, timeout=CACHE_TIMEOUT)
        except URL.DoesNotExist:
            return notfound({"error": "URL not found"})
    
    increment_click_count.delay(shortened_url)
    
    return success({"original_url": original_url})


@api_view(['GET'])
def url_stats(request, shortened_url):
    serializer = URLRetrieveSerializer(data={"shortened_url": shortened_url})
    serializer.is_valid(raise_exception=True)

    try:
        url = URL.objects.get(shortened_url=shortened_url)
        return success({"clicks": url.click_count})
    except URL.DoesNotExist:
        return notfound({"error": "URL not found"})
