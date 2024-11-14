import pytest
from django.urls import reverse
from django.test import AsyncClient
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
    
    async def test_shorten_url(self):
        client = AsyncClient()
        response = await client.post(SHORTEN_URL_ENDPOINT, data={"original_url": TEST_ORIGINAL_URL}, content_type="application/json")
        assert response.status_code == status.HTTP_200_OK
        assert "shortened_url" in response.json()

    async def test_get_original_url(self):
        url = await URL.objects.acreate(original_url=TEST_ORIGINAL_URL, shortened_url=EXPECTED_SHORTENED_URL)
        client = AsyncClient()
        response = await client.get(f"{GET_ORIGINAL_URL_ENDPOINT}/{EXPECTED_SHORTENED_URL}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["original_url"] == TEST_ORIGINAL_URL

    async def test_url_stats(self):
        url = await URL.objects.acreate(original_url=TEST_ORIGINAL_URL, shortened_url=EXPECTED_SHORTENED_URL_2, click_count=5)
        client = AsyncClient()
        response = await client.get(f"{URL_STATS_ENDPOINT}/{EXPECTED_SHORTENED_URL_2}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["clicks"] == 5
