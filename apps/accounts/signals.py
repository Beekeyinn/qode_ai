from cgi import print_arguments

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import social_account_added
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User
