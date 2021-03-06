from django.contrib import admin

from .models import Card, Bin


class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'definition', 'bin', 'next_review', 'total_wrong')


admin.site.register(Card, CardAdmin)


class BinAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'unit')


admin.site.register(Bin, BinAdmin)
