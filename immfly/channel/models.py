from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import JSONField

from common.models import Language


class TreeChannel(models.Model):
    """
    TreeChannel stands for the hierarchy tree of channel
    entertainments system, containing the parent root.
    """

    root = models.ForeignKey('ChannelNode', blank=True, related_name='tree', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)


class ChannelNode(models.Model):
    """
    ChannelNode contains the information of a channel
    inside the tree hierarchy of the entertaiment system.

    NOTE: only a ChannelNode with no children in it can
    have set the attribute contents.
    """

    parent = models.ForeignKey('self', blank=True, related_name='children', on_delete=models.CASCADE)

    title = models.CharField(max_length=250)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    picture = models.ImageField(blank=True)
    thumbnail = models.ImageField(blank=True, height_field=100, width_field=100)

    contents = models.ForeignKey('Content', related_name='channel', blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.children is not None and self.contents:
            return # A ChannelNode with children can not have contents.

        super().save(*args, **kwargs)


class Content(models.Model):
    """
    Content is a set of files such as (text, pdfs, video, ...) that are
    related to a subchannel that does not have more reference channels
    below to it.
    """

    item = models.FileField()
    meta_info = JSONField(blank=True, null=True)
    rating_value = models.DecimalField(
        default=Decimal('0.00'),
        max_digits=2,
        decimal_places=2,
        validators=[MinValueValidator('0.00'), MaxValueValidator('10.00')],
    )
