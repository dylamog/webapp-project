from django.contrib import admin

from .models import Thread



class ThreadAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Thread, ThreadAdmin)

