from rest_framework.generics import ListCreateAPIView

from api.serializers import ChannelNodeDetailSerializer, \
    ContentDetailSerializer, TreeChannelDetailSerializer, LanguageDetailSerializer
from channel.models import ChannelNode, Content, TreeChannel
from common.models import Language


class TreeChannelViewSet(ListCreateAPIView):

    name = 'tree-view'
    queryset = TreeChannel.objects.all()
    serializer_class = TreeChannelDetailSerializer


class ChannelNodeViewSet(ListCreateAPIView):
 
    name = 'channel-node-view'
    queryset = ChannelNode.objects.all()
    serializer_class = ChannelNodeDetailSerializer


class ContentViewSet(ListCreateAPIView):

    name = 'content.view'
    queryset = Content.objects.all()
    serializer_class = ContentDetailSerializer


class LanguageViewSet(ListCreateAPIView):

    name = 'language-view'
    queryset = Language.objects.all()
    serializer_class = LanguageDetailSerializer
