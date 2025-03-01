"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from base import views
import os

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),
    
    path('', views.IndexListView.as_view()),
    path('items/<str:pk>/', views.ItemDetailView.as_view()),
    path('categories/<str:pk>/', views.CategoryListView.as_view()),
    path('tags/<str:pk>/', views.TagListView.as_view()),

    path('cart/', views.CartListView.as_view()),
    path('cart/add/', views.AddCartView.as_view()),
    path('cart/remove/<str:pk>/', views.remove_from_cart),

    path('pay/checkout/', views.PayWithStripe.as_view()),
    path('pay/success/', views.PaySuccessView.as_view()),
    path('pay/cancel/', views.PayCancelView.as_view()),

    path('orders/', views.OrderIndexView.as_view()),
    path('orders/<str:pk>/', views.OrderDetailView.as_view()),

    path('downloads/capture/<str:id>/', views.Download.as_view()),

    path('about_us/', views.AboutUsView.as_view()),
    path('legal_information/', views.LegalInformationView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=os.path.join(settings.MEDIA_ROOT, 'media'))

    

