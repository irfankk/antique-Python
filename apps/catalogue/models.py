from django.db import models
from django.utils.translation import ugettext_lazy as _l, ugettext as _


class Product(models.Model):
	ACTIVE, DEACTIVATED = range(2)
	STATUS_CHOICES = (
		(ACTIVE, _('Active')),
		(DEACTIVATED, _('Deactivated')),
		)
	status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, default=ACTIVE)
	title = models.CharField(_('Product title'), max_length=255)
	stock = models.IntegerField(_('number of stocks'), default=0)
	price = models.IntegerField( verbose_name=_('Price'), null=True )
	age = models.IntegerField(verbose_name=_('Age'),null=True)
	description = models.TextField(_('Description'), blank=True)
	image = models.ImageField(_("Original"), upload_to='product_images',max_length=255)

