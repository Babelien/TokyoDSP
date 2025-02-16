from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
 
class CartListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/cart.html'

    def get_queryset(self):
        cart = self.request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            return redirect('/')
        
        self.queryset = []
        self.total = 0

        for item_pk, formats in cart['items'].items():
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = 1
            obj.purchase_formats = formats
            obj.subtotal = int(obj.price * len(formats))
            self.queryset.append(obj)
            self.total += obj.subtotal

        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
        
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['total'] = self.total
            context['tax_included_total'] = self.tax_included_total
        except Exception:
            pass

        return context

class AddCartView(View):
    def post(self, request):
        item_pk = request.POST.get('item_pk')
        formats = request.POST.getlist('formats')
        if not formats:
            messages.error(request, 'Not select formats')
            return redirect(f'/items/{item_pk}/')

        cart = request.session.get('cart', None)

        if cart is None or len(cart) == 0:
            items = OrderedDict()
            cart = {'items': items}

        cart['items'][item_pk] = formats

        request.session['cart'] = cart

        return redirect('/cart/')

@login_required
def remove_from_cart(request, pk):
    cart = request.session.get('cart', None)
    if cart is not None:
        del cart['items'][pk]
        request.session['cart'] = cart
    
    return redirect('/cart/')