from celery import shared_task
from .models import URL

"""celery task to increment click counts"""
@shared_task
def increment_click_count(shortened_url):
    url = URL.objects.get(shortened_url=shortened_url)
    url.click_count += 1
    url.save()
