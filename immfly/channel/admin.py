from django.contrib import admin

from channel.models import ChannelNode, Content, TreeChannel

@admin.register(TreeChannel)
class TreeChannelAdmin(admin.ModelAdmin):

    list_display = (
        'name', # This is made because we want to avoid the __str__ method.
    )

admin.site.register(ChannelNode)
admin.site.register(Content)
