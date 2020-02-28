import factory

from channel.models import TreeChannel, ChannelNode, Content


class ContentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Content


class ChannelNodeFactory(factory.DjangoModelFactory):

    class Meta:
        model = ChannelNode

    parent = factory.LazyAttribute(lambda x: ChannelNodeFactory(parent=None))
    # language = 
    # picture

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

    root = factory.SubFactory(ChannelNodeFactory)
