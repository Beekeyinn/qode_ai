import random
import string

from django.utils.text import slugify


def rand_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None, field_name="title"):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, field_name))

    Klass = instance.__class__
    qs_exist = Klass.objects.filter(slug=slug).exists()
    if qs_exist:
        new_slug = f"{slug}-{rand_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
