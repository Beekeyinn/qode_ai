import os

from django.conf import settings
from openai import OpenAI

client = OpenAI(
    api_key=getattr(settings, "OPENAI_API_KEY", ""), max_retries=3, timeout=180
)
