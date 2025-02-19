from django.shortcuts import redirect
from django.conf import settings
from django.core import serializers
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from base.models import Item, Order
import stripe
import json

stripe.api_key = settings.STRIPE_API_SECRET_KEY

def delete_unconfirmed_order(user_id):
    orders = Order.objects.filter(user=user_id, is_confirmed=False)
    for order in orders:
        order.delete()


class PaySuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/success.html'

    def get(self, request, *args, **kwargs):
        order_id = request.GET.get('order_id')
        orders = Order.objects.filter(user=request.user, id=order_id)
        if len(orders) != 1:
            return super().get(request, *args, **kwargs)

        order = orders[0]
        order.is_confirmed = True
        order.save()

        for elem in json.loads(order.items):
            item = Item.objects.get(pk=elem['pk'])
            item.sold_count += 1
            item.save()

        delete_unconfirmed_order(request.user)

        del request.session['cart']

        return super().get(request, *args, **kwargs)
    
class PayCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/cancel.html'

    def get(self, request, *args, **kwargs):
        delete_unconfirmed_order(request.user)
        return super().get(request, *args, **kwargs)
    
tax_rate = stripe.TaxRate.create(
    display_name='Tax',
    description='Tax',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE * 100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)
 
 
def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            'currency': 'USD',
            'unit_amount': unit_amount * 100,
            'product_data': {'name': name, }
        },
        'quantity': quantity,
        'tax_rates': [tax_rate.id]
    }
 
 
class PayWithStripe(LoginRequiredMixin, View):
 
    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            messages.error(request, 'Cart is nothing')
            return redirect('/')
 
        items = []
        line_items = []
        for item_pk, formats in cart['items'].items():
            item = Item.objects.get(pk=item_pk)
            line_item = create_line_item(
                item.price, item.name, len(formats))
            line_items.append(line_item)

            items.append(
                {
                    'pk':item.pk,
                    'name':item.name,
                    'image':str(item.image),
                    'price':item.price,
                    'formats': formats,
                }
            )

        delete_unconfirmed_order(request.user)

        order = Order.objects.create(
            user=request.user,
            uid=request.user.pk,
            items=json.dumps(items),
            shipping=serializers.serialize('json', [request.user.profile]),
            amount=cart['total'],
            tax_included=cart['tax_included_total']
        )
 
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{settings.MY_URL}pay/success/?order_id={order.pk}',
            cancel_url=f'{settings.MY_URL}pay/cancel/',
        )
        return redirect(checkout_session.url)