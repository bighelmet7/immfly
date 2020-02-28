from django.test import TestCase

from channel.factories import ChannelNodeFactory, ContentFactory


class ChannelNodeTest(TestCase):

    def test_save_channel_with_children_a_content(self):
        """
        A ChannelNode with children can not have set the attribute
        contents.
        """
        serie = ChannelNodeFactory()
        serie.save()
        sub_serie = ChannelNodeFactory(parent=serie)
        sub_serie.save()
        content = ContentFactory()
        # content.channel.add(serie)
        content.save()
        self.assertEqual(serie.contents, 0)
