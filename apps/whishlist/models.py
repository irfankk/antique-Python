from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from apps.catalogue.models import Product


class Wishlist(models.Model):
    user = models.OneToOneField(User, 
        related_name='wishlist', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Wishlist')
        verbose_name_plural = _('Wishlists')

    def __unicode__(self):
        return _(
            'Wishlist (owner: {user}, lines: {lines})'
        ).format(
            user=self.user,
            lines=self.lines.count()
        )


    @property
    def total_quantity(self):
        quantity = 0
        for line in self.lines.all():
            quantity += line.quantity
        return quantity

class Line(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        related_name='lines', on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='wishlist_lines', on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        default=1
    )

    class Meta:
        verbose_name = _('Wishlist line')
        verbose_name_plural = _('Wishlist lines')

    def __unicode__(self):
        return _(
            'Wishlist #{wishlist_id}, Product #{product_id}, '\
            'quantity {quantity}'
        ).format(
            wishlist_id=self.wishlist.pk,
            product_id=self.product.pk,
            quantity=self.quantity,
        )

    def get_price(self):
        price = self.product.price
        if self.product.on_sale_valid():
            price = self.product.sale_price
        return price * self.quantity
