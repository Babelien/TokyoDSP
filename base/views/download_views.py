from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from base.models import Capture, Order
import json

class Download(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        capture = Capture.objects.get(id=kwargs['id'])
        
        orders = Order.objects.filter(user=request.user)
        for order in orders:
            items = json.loads(order.items)
            for item in items:
                if item['pk'] == capture.item.pk:
                    for format in item['formats']:
                        if format == capture.format.name:
                            return FileResponse(capture.data)
                    
        messages.error(request, 'Invalid request')
        return redirect('/')