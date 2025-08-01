import uuid as uuid
from django.db import models
from django.core.signing import Signer


class ProductLink(models.Model):
    objects = models.Manager()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    product_id = models.IntegerField()

    @classmethod
    def create_for_product(cls, product_id):
        new_link = cls.objects.create(product_id=product_id)
        return new_link.uuid
