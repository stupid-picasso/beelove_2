from django.contrib import admin
from .models import MatchList , MatchRequest
# Register your models here.


class MatchSystemAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = MatchList

admin.site.register(MatchList,MatchSystemAdmin)


class MatchRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender','receiver']
    list_display = ['sender','receiver']
    search_fields = ['sender__username','sender__email','receiver__email','receiver__username']

    class Meta:
        model = MatchRequest

admin.site.register(MatchRequest,MatchRequestAdmin)