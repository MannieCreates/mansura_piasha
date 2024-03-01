from django.contrib import admin
from .models import login_info, Item, Poll, Choice


# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice


class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(login_info)
admin.site.register(Item)

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
