from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from .models import URL
from django.core.cache import cache
from .task import increment_click_count
from .response_functions import success, notfound
from .serializer import URLShortenSerializer, URLRetrieveSerializer

CACHE_TIMEOUT = 60 * 60  # Cache timeout set to 1 hour

@api_view(['POST'])
def shorten_url(request):
    """
    Handle POST requests to shorten a given URL.
    
    - Validates the input URL using `URLShortenSerializer`.
    - Generates a unique shortened URL using `get_random_string`.
    - Stores the mapping of the shortened URL to the original URL in the database.
    - Adds the shortened URL and original URL to the cache for faster retrieval.
    - Returns the shortened URL in the response.
    """
    print("shorten_url view called")  # Add debug log
    serializer = URLShortenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    print("shorten_url view called")  # Add debug log

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
    """
    Handle GET requests to retrieve the original URL for a given shortened URL.
    
    - First checks if the shortened URL exists in the cache.
    - If not, validates the input using `URLRetrieveSerializer` and queries the database.
    - If the shortened URL is found in the database, it is added to the cache.
    - If the URL is not found, returns a 404 response.
    - Triggers a background task to increment the click count for the shortened URL.
    - Returns the original URL in the response.
    """
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
    """
    Handle GET requests to retrieve statistics for a given shortened URL.
    
    - Validates the input using `URLRetrieveSerializer`.
    - Queries the database for the shortened URL to get its click count.
    - If the shortened URL does not exist, returns a 404 response.
    - Returns the click count for the shortened URL in the response.
    """
    serializer = URLRetrieveSerializer(data={"shortened_url": shortened_url})
    serializer.is_valid(raise_exception=True)

    try:
        url = URL.objects.get(shortened_url=shortened_url)
        return success({"clicks": url.click_count})
    except URL.DoesNotExist:
        return notfound({"error": "URL not found"})
