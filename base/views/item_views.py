from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from base.models import Item, Order, Category, Capture, Tag
import json

class IndexListView(ListView):
    model = Item
    template_name = 'pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().order_by('order')
        category_dict_list = []
        for category_obj in categories:
            items = Item.objects.filter(category=category_obj.pk, is_published=True).order_by('-created_at')
            dic = {category_obj:items}
            category_dict_list.append(dic)
        context['dict_list'] = category_dict_list
        return context



class ItemDetailView(DetailView):
    model = Item
    template_name = 'pages/item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()

        # 購入済フォーマットをpurchased_formatsに追加
        context['purchased_captures'] = []
        context['purchased_formats'] = []

        if self.request.user.pk:
            orders = Order.objects.filter(user=self.request.user, is_confirmed=True)
            for order in orders:
                order_items = json.loads(order.items)
                for order_item in order_items:
                    if order_item['name'] == item.name:
                        for format in order_item['formats']:
                            captures = Capture.objects.filter(item=item.pk, format=format)
                            if len(captures) == 1:
                                capture = captures[0]
                                if capture not in context['purchased_captures']:
                                    context['purchased_captures'].append(capture)
                                    context['purchased_formats'].append(format)

        return context
    
class CategoryListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 10
 
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(is_published=True, category=self.category)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Category #{self.category.name}'
        return context
 
 
class TagListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 10
 
    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(is_published=True, tags=self.tag)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Tag #{self.tag.name}"
        return context