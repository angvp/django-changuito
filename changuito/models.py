from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

try:
    from django.conf import settings
    User = settings.AUTH_USER_MODEL
except (ImportError, AttributeError):
    from django.contrib.auth.models import User

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    creation_date = models.DateTimeField(verbose_name=_('creation date'),
                                         default=timezone.now)
    checked_out = models.BooleanField(default=False,
                                      verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)
        app_label = 'changuito'

    def __unicode__(self):
        return "Cart id: %s" % self.id

    def is_empty(self):
        return self.item_set.count() == 0

    def total_price(self):
        return sum(i.total_price for i in self.item_set.all())

    def total_quantity(self):
        return sum(i.quantity for i in self.item_set.all())


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']),
                                                                       for_concrete_model=False)
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.DecimalField(max_digits=18, decimal_places=3,
                                   verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2,
                                     verbose_name=_('unit price'))
    # product as generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)
        app_label = 'changuito'

    def __unicode__(self):
        return u'{0} units of {1} {2}'.format(self.quantity,
                                              self.product.__class__.__name__,
                                              self.product.pk)

    def total_price(self):
        return float(self.quantity) * float(self.unit_price)
    total_price = property(total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product),
                                                              for_concrete_model=False)
        self.object_id = product.pk

    product = property(get_product, set_product)

    def update_quantity(self, quantity):
        self.quantity = quantity
        self.save()

    def update_price(self, price):
        self.unit_price = price
        self.save()

    def update_contenttype(self, ctype_obj):
        new_content_type = ContentType.objects.get_for_model(type(ctype_obj),
                                                             for_concrete_model=False)
        # Let's search if the new contenttype had previous items on the cart
        try:
            new_items = Item.objects.get(cart=self.cart,
                                         object_id=self.object_id,
                                         content_type=new_content_type)
            self.quantity += new_items.quantity
            new_items.delete()
        except self.DoesNotExist:
            pass

        self.content_type = new_content_type
        self.save()
