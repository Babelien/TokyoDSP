from django.contrib import admin
from base.models import Item, Category, Tag, Format, Order, Capture
from django.contrib.auth.models import Group
# Register your models here.

class TagInline(admin.TabularInline):
    model = Item.tags.through
 
 
class ItemAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags']

admin.site.register(Item, ItemAdmin)
admin.site.register(Capture)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Format)
admin.site.register(Order)
admin.site.unregister(Group)

