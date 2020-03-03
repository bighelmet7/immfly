from django.urls import path

from api.views import ChannelNodeViewSet, ContentViewSet, TreeChannelViewSet, LanguageViewSet

urlpatterns = [
    path('v1/channel/', ChannelNodeViewSet.as_view(), name=ChannelNodeViewSet.name),
    path('v1/content/', ContentViewSet.as_view(), name=ContentViewSet.name),
    path('v1/tree/', TreeChannelViewSet.as_view(), name=TreeChannelViewSet.name),
    path('v1/language/', LanguageViewSet.as_view(), name=LanguageViewSet.name),
]
