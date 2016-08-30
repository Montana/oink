from django.contrib import admin
from django.contrib.admin import AdminSite
from adminplus.sites import AdminSitePlus
from main.models import *
from django.utils.translation import ugettext_lazy

# Register your models here.
class MyAdminSite(AdminSitePlus):
	site_title = ugettext_lazy('Okcupid Bots Administration')
	site_header = ugettext_lazy('Okcupid Bots Administration')
	index_title = ugettext_lazy('Okcupid Bots Administration')
	
admin_site = MyAdminSite()


class MessageAdmin(admin.ModelAdmin):
	list_display = ('username','password','body','interval')
	ordering = ('username',)
	search_fields = ('username',)
	
admin_site.register(MessageSetting,MessageAdmin)


class MessageSentAdmin(admin.ModelAdmin):
	list_display = ('sender','receiver','message','datetime')
	ordering = ('sender',)
	search_fields = ('sender',)
	
admin_site.register(MessageSent,MessageSentAdmin)
	
