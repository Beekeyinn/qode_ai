from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ParameterTypeChoices(TextChoices):
    OBJECT = "object", _("Object")
    STRING = "string", _("String")
    INTEGER = "integer", _("Integer")
    NUMBER = "number", _("Number")
    BOOLEAN = "boolean", _("Boolean")
    ARRAY = "array", _("Array")


class PropertyValueFormatType(TextChoices):
    # String representation
    DATE = "date", _("Date")
    DATETIME = "date-time", _("Datetime")
    PASSWORD = "password", _("Password")
    BYTE = "byte", _("Byte")
    BINARY = "binary", _("Binary")
    EMAIL = "email", _("Email")
    UUID = "uuid", _("UUID")
    URI = "uri", _("URI")
    HOSTNAME = "hostname", _("Hostname")
    IPV4 = "ipv4", _("IPv4")
    IPV6 = "ipv6", _("IPv6")
    # Number representation
    FLOAT = "float", _("Float")
    DOUBLE = "double", _("Double")

    # Integer representation
    INT32 = "int32", _("Integer 32")
    INT64 = "int64", _("Integer 64")
