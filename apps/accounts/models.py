from base64 import b64decode, b64encode

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext_lazy as _

# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build

from apps.core.models import ExtraFieldsModelsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("User must have an username.")
        user = self.model(email=self.normalize_email(email), username=username, **extra)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra.setdefault("is_admin", True)
        extra.setdefault("is_superuser", True)
        user = self.create_user(email, password=password, username=username, **extra)
        return user


class User(AbstractBaseUser, PermissionsMixin, ExtraFieldsModelsMixin):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=255,
        unique=True,
        null=False,
        blank=False,
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email}"

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def encoded_email(self):
        return force_str(b64encode(force_bytes(self.email)))

    def decode_email(self, encoded_email):
        return force_str(b64decode(encoded_email))

    # @property
    # def google_calendar(self):
    #     if hasattr(self, "socialaccount_set"):
    #         social_account = self.socialaccount_set.filter(
    #             provider="Google Authentication"
    #         ).first()
    #         if social_account:
    #             if hasattr(social_account, "socialtoken_set"):
    #                 token = social_account.socialtoken_set.get()
    #                 app = token.app
    #                 creds = Credentials(
    #                     token=token.token,
    #                     refresh_token=token.token_secret,
    #                     client_id=app.client_id,
    #                     client_secret=app.secret,
    #                     token_uri="https://oauth2.googleapis.com/token",
    #                 )
    #                 return build("calendar", "v3", credentials=creds), {"success": True}
    #             return None, {"success": False, "error": "No token found"}
    #         return None, {"success": False, "error": "No social account found"}
    #     return None, {"success": False, "error": "No social account attributes found"}
