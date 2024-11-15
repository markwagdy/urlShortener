import pytest
from django.test import AsyncClient
from django.urls import reverse
from rest_framework import status
from .models import URL
from const_tests import (
    SHORTEN_URL_ENDPOINT,
    GET_ORIGINAL_URL_ENDPOINT,
    URL_STATS_ENDPOINT,
    TEST_ORIGINAL_URL,
    EXPECTED_SHORTENED_URL,
    EXPECTED_SHORTENED_URL_2,
)


@pytest.mark.asyncio
@pytest.mark.django_db
class TestURLShortener:
    """Success test case for each endpoint"""
    async def test_shorten_url(self):
        client = AsyncClient()
        response = await client.post(
            reverse('shorten_url'),
            data={"original_url": TEST_ORIGINAL_URL},
            content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert "shortened_url" in response.json()['data']

    async def test_get_original_url(self):
        await URL.objects.acreate(original_url=TEST_ORIGINAL_URL, shortened_url=EXPECTED_SHORTENED_URL)
        client = AsyncClient()
        url=reverse('get_original_url',args=[EXPECTED_SHORTENED_URL])
        response = await client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']["original_url"] == TEST_ORIGINAL_URL

    async def test_url_stats(self):
        await URL.objects.acreate(original_url=TEST_ORIGINAL_URL, shortened_url=EXPECTED_SHORTENED_URL_2, click_count=5)
        client = AsyncClient()
        url = reverse('url_stats', args=[EXPECTED_SHORTENED_URL_2])
        response = await client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']["clicks"] == 5
