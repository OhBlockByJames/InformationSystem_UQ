from django.contrib import admin
from .models import Customer, Order, Product, Material, Consume, Use,Retention

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Material)
admin.site.register(Consume)
admin.site.register(Use)
admin.site.register(Retention)
