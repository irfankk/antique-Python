from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

from apps.catalogue.models import Product

class Basket(TimeStampedModel):
	OPEN, SUBMITTED = range(2)
	STATUS_CHOICES = (
		(OPEN, _("Open - currently active")),
		(SUBMITTED, _("Submitted - has been ordered at the checkout")),
		)
	status = models.PositiveSmallIntegerField(_('status'), default=OPEN, choices=STATUS_CHOICES)
	owner = models.ForeignKey(User,verbose_name=_('Owner'),
		related_name='basket',null=True, on_delete=models.CASCADE)
	date_submitted = models.DateTimeField(_("Date submitted"),null=True,blank=True)

	class Meta:
		verbose_name = _('Basket')
		verbose_name_plural = _('Baskets')
	def __str__(self):
		return self.get_status_display()
	def cart_total_price(self):
		price = 0
		for item in self.lines.all():
			price += (item.quantity * item.price)
		return price


class Line(TimeStampedModel):
    """
    A line of a basket (product and qty)
    """
    basket = models.ForeignKey(Basket, related_name='lines',verbose_name=_("Basket"),
     on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='basket_lines',verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    price = models.DecimalField(verbose_name=_('Price'),max_digits=15,decimal_places=3,null=True)
    class Meta:
    	verbose_name = _('Basket line')
    	verbose_name_plural = _('Basket lines')

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        return self.quantity * self.price