from django.contrib import admin
from main.models import *

class TopicPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'due','answer','active')


admin.site.register(Player)
admin.site.register(Topic, TopicPostAdmin)
admin.site.register(Player_Topic)

