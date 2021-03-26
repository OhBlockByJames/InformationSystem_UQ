"""UQ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views
urlpatterns = [
	path('', views.index, name='index'),
	path('home', views.home, name='home'),
	path('sales', views.sales, name='sales'),
	path('marketing', views.marketing, name='marketing'),
	path('production', views.EPQ_calculate, name='production'),
	path('update', views.cal_inventory, name='update'),
	path('profit', views.Profit, name='profit'),
	path('plot', views.raw_plot, name='plot'),
	# path('profit', views.dropdownMenu, name='profit'),
	path('order', views.EOQ_calculate, name='order'),
	path('rfm', views.c_rfm, name='rfm'),
	path('monthsales', views.index, name='monthsales'),
	path('material', views.Raw_EOQ, name='material'),
	path('customer', views.customer, name='customer'),
	path('retention', views.cus_retention, name='retention'),
]
