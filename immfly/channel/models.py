from decimal import Decimal, localcontext

from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

from common.models import Language


class TreeChannel(models.Model):
    """
    TreeChannel stands for the hierarchy tree of channel
    entertainments system, containing the parent root.
    """

    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return '<TreeChannel %s> %s' % (self.id, self.name)


class ChannelNode(models.Model):
    """
    ChannelNode contains the information of a channel
    inside the tree hierarchy of the entertaiment system.

    NOTE: only a ChannelNode with no children in it can
    have set the attribute contents.
    """

    tree = models.ForeignKey(
        'TreeChannel',
        blank=True,
        null=True,
        related_name='root',
        on_delete=models.CASCADE
    )

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=250, unique=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    picture = models.ImageField(blank=True)
    thumbnail = models.ImageField(blank=True, height_field=100, width_field=100)

    def save(self, *args, **kwargs):

        if self.children.count() and self.contents.count():
            raise ValueError('A parent ChannelNode can not have contents in it.')

        super().save(*args, **kwargs)

    def _irate_value(self, node, calculated_values):
        """
        Base case: if node is a leaf then returns the AVG of its contents.
        Induction: the Avg of a parent node depends on the avg of its children.

        *Returns the AVG of the current node.

        *Modifies a dict passed by reference where contains as a key the node id and
        as a value the AVG of the node.
        """
        with localcontext() as ctx: # This is need for Decimal standarization.
            ctx.prec = 4
            if not node.children.count():
                content_avg = node.contents.all().aggregate(Avg('rating_value'))
                result = content_avg['rating_value__avg']
                calculated_values[node.title] = result
                return result

            _rate_sum = Decimal('0')
            for child in node.children.all():
                _rate_sum += self._irate_value(child, calculated_values)

            result = Decimal(_rate_sum / node.children.count())
            calculated_values[node.title] = result
            return result

    @property
    def rating_value(self):
        """
        Calculate the rating value of a channel.

        Return the rating value of the given node, and an history
        of all the calculated rating values of the hierarchy of the
        current node.
        """

        calculated_values = dict()
        result = self._irate_value(self, calculated_values)

        return result, calculated_values

    def __str__(self):
        return '<ChannelNode %s> %s' % (self.id, self.title)


class Content(models.Model):
    """
    Content is a set of files such as (text, pdfs, video, ...) that are
    related to a subchannel that does not have more reference channels
    below to it.
    """

    item = models.FileField(blank=True)
    meta_info = JSONField(blank=True, null=True)
    rating_value = models.DecimalField(
        default=Decimal('0'),
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('10'))],
    )
    channel = models.ForeignKey(
        'ChannelNode',
        blank=True,
        null=True,
        related_name='contents',
        on_delete=models.CASCADE
    )

    def __str__(self):
        # TODO: extract title or smth equivalent in meta_info.
        return '<Content %s> Channel %s' % (self.id, self.channel.title)
