import factory

from channels.models import TreeChannel, ChannelNode, Content


class ContentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Content


class ChannelNodeFactory(factory.DjangoModelFactory):

    class Meta:
        model = ChannelNode

    parent = factory.LazyAttribute(lambda x: ChannelNodeFactory(parent=None))
    contents = factory.SubFactory(ContentFactory)


class TreeChannelFactory(factory.DjangoModelFactory):

    class Meta:
        model = TreeChannel

    root = factory.SubFactory(ChannelNodeFactory)
