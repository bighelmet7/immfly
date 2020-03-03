import factory

from common.factories import LanguageFactory
from channel.models import TreeChannel, ChannelNode, Content


class ContentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Content


class ChannelNodeFactory(factory.DjangoModelFactory):

    class Meta:
        model = ChannelNode

    parent = factory.LazyAttribute(lambda x: ChannelNodeFactory(parent=None))
    title = factory.Faker('name')
    language = factory.SubFactory(LanguageFactory)

    @factory.post_generation
    def contents(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for content in extracted:
                self.contents.add(content)


class TreeChannelFactory(factory.DjangoModelFactory):

    class Meta:
        model = TreeChannel

    name = factory.Faker('name')
