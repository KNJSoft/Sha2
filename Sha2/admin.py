from django.contrib import admin
from .models import *
# Register your models here.
class FichierAdmin(admin.ModelAdmin):
    list_display = ('nom','path','user','date_creation')
    search_fields = ['nom',]

class MessageAdmin(admin.ModelAdmin):
    list_display = ('texte','hash')
    search_fields = ['texte',]

admin.site.register(Fichier,FichierAdmin)
admin.site.register(Message,MessageAdmin)


ets="SR3A-SHA2"
admin.site.site_header=ets
admin.site.site_title=ets
admin.site.index_title=ets