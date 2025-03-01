from django.conf import settings
from base.models import Item

def base(request):
    items = Item.objects.filter(is_published=True)

    return {
        'TITLE': settings.TITLE,
        'ADDITIONAL_ITEMS': items,
        'POPULAR_ITEMS': items.order_by('-sold_count'),
        'RECENT_ITEMS': items.order_by('-created_at'),
    }