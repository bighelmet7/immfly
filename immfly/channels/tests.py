from django.test import TestCase

from factories import ChannelNodeFactory, ContentFactory


class ChannelNodeTest(TestCase):

    def test_save_channel_with_children_a_content(self):
        """
        A ChannelNode with children can not have set the attribute
        contents.
        """
        serie = ChannelNodeFactory()
        sub_serie = ChannelNodeFactory(parent=serie)
        content = ContentFactory()
        serie.contents.add(content) # this shouldnt be added to our DB
        self.assertEqual(len(serie.contents.all()), 0)
