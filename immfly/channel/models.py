from decimal import Decimal
from queue import Queue

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

    name = models.CharField(max_length=250)


class ChannelNode(models.Model):
    """
    ChannelNode contains the information of a channel
    inside the tree hierarchy of the entertaiment system.

    NOTE: only a ChannelNode with no children in it can
    have set the attribute contents.
    """

    root = models.ForeignKey(
        'TreeChannel',
        blank=True,
        null=True,
        related_name='tree',
        on_delete=models.CASCADE
    )

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=250)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    picture = models.ImageField(blank=True)
    thumbnail = models.ImageField(blank=True, height_field=100, width_field=100)

    def save(self, *args, **kwargs):

        if self.children.count() and self.contents.count():
            raise ValueError('A parent ChannelNode can not have contents in it.')

        super().save(*args, **kwargs)

    def _irate_value(self, node):
        """
        Base case: if node is a leaf then returns the AVG of its contents.
        Induction: the Avg of a parent node depends on the avg of its children.
        """
        if not node.children.count():
            content_avg = node.contents.all().aggregate(Avg('rating_value'))
            return content_avg['rating_value__avg']

        n_nodes = 0
        _rate_sum = Decimal('0')
        for child in node.children.all():
            n_nodes += child.children.count()
            _rate_sum += self._irate_value(child)
        n_nodes += node.children.count()
        return Decimal(_rate_sum / n_nodes)

    @property
    def rating_value(self):
        """
        Calculate the rating value of a channel.
        """
        return self._irate_value(self)


class Content(models.Model):
    """
    Content is a set of files such as (text, pdfs, video, ...) that are
    related to a subchannel that does not have more reference channels
    below to it.
    """

    item = models.FileField()
    meta_info = JSONField(blank=True, null=True)
    rating_value = models.DecimalField(
        default=Decimal('0'),
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('10'))],
    )
    channel = models.ForeignKey(
        'ChannelNode',
        related_name='contents',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
