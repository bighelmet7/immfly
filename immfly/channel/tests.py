from decimal import Decimal

from django.test import TestCase
from django.db.models import Avg

from channel.factories import ChannelNodeFactory, ContentFactory, TreeChannelFactory
from common.factories import LanguageFactory


class ChannelNodeTest(TestCase):

    def test_set_content_to_a_channel_that_is_a_parent_node(self):
        """
        Serie (parent) -> sub_serie (children); serie cant have contents
        because is a parent node.
        """
        # Having a language, content and a parent node.
        language = LanguageFactory()
        content = ContentFactory()
        serie = ChannelNodeFactory(
            language=language,
        )
        # Add a children to serie (parent node)
        sub_serie = ChannelNodeFactory(
            parent=serie
        )
        # When adding a content to a parent node, this should raise a
        # ValueError exception, because a parent can not have a set
        # of contents just leaves.
        with self.assertRaises(ValueError):
            serie.contents.add(content)
            serie.save()

    def test_set_content_to_a_channel_that_is_not_a_parent_node(self):
        """
        Serie (parent) -> sub_serie (children); subserie can have contents
        because is a leaf node.
        """
        # Having a language, content and a parent node.
        language = LanguageFactory()
        content = ContentFactory()
        serie = ChannelNodeFactory(
            language=language,
        )
        # Add a children to serie and set content to this child.
        sub_serie = ChannelNodeFactory(
            parent=serie,
            contents=[content]
        )
        # sub_serie should contain a content and a parent reference to it.
        result = (sub_serie.contents.count(), sub_serie.parent.id)
        expected = (1, serie.id)
        self.assertEqual(result, expected)

    def test_setting_a_channel_hierarchy(self):
        """
        The exam give us an example of how does a channel hierarchy looks like
        then we are going to represent that example with our models.

        Root → Series → Atresplayer → El club de la comedia → El club de la comedia (Chapter 1)
        """
        language = LanguageFactory()
        root = TreeChannelFactory(
            name='Root'
        )
        series = ChannelNodeFactory(
            root=root,
            title='Series',
            language=language,
        )
        sub_serie = ChannelNodeFactory(
            parent=series,
            title='Atresplayer',
        )
        comedy = ChannelNodeFactory(
            parent=sub_serie,
            title='El club de la comedia',
        )
        content = ContentFactory()
        chapter = ChannelNodeFactory(
            parent=comedy,
            title='El club de la comedia (Chapter 1)',
            contents=[content]
        )
        # The last node of the hierarchy can access to the highest parent of the structure.
        self.assertEqual(chapter.parent.parent.parent.id, series.id)

    def test_get_average_of_the_contents_of_a_subchannel(self):
        """
        If we're in a subchannel (leaf node) it contains a set of contents,
        which we must know the average of all rating values.
        """
        # Having a language, parent and a leaf node, and a set of contents
        language = LanguageFactory()
        parent = ChannelNodeFactory(
            language=language,
        )
        content_1 = ContentFactory(
            rating_value=Decimal('3.14')
        )
        content_2 = ContentFactory(
            rating_value=Decimal('5.12')
        )
        leaf = ChannelNodeFactory(
            parent=parent,
            contents=[content_1, content_2],
        )
        # Then the rating value of the subchannel (leaf) must be the average of
        # the contents rating value.
        result = leaf.contents.all().aggregate(Avg('rating_value'))
        expected = Decimal((content_1.rating_value + content_2.rating_value) / 2)
        self.assertEqual(result['rating_value__avg'], expected)

    def test_get_rating_average_of_a_channel(self):
        """
        A channel can not store rating values, so this is calculated as
        the average of the rating values of its subchannels.
        """
        # Having a language, parent and a leaf node, and a set of contents
        language = LanguageFactory()
        parent = ChannelNodeFactory(
            language=language,
        )
        content_1 = ContentFactory(
            rating_value=Decimal('3.14')
        )
        content_2 = ContentFactory(
            rating_value=Decimal('5.12')
        )
        content_3 = ContentFactory(
            rating_value=Decimal('8.3')
        )
        leaf_1 = ChannelNodeFactory(
            parent=parent,
            contents=[content_1, content_2],
        )
        leaf_2 = ChannelNodeFactory(
            parent=parent,
            contents=[content_3],
        )
        self.assertEqual(parent.rating_value, Decimal('6.215'))
