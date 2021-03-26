from django.db import models
from django.utils.translation import gettext_lazy as trans
from datetime import date
from django.utils import timezone
# Create your models here.
class Customer(models.Model):
	c_id = models.CharField(max_length = 10,primary_key=True) 
	c_name = models.CharField(max_length = 20) 
	c_age = models.CharField(max_length = 3) 
	c_phone = models.CharField(max_length = 20)
	#c_fdate = models.CharField(max_length = 20)
	c_fdate = models.DateField(default=date.today)
	def __str__(self):
		return self.c_id

class Product(models.Model):
	#category =  models.TextField(max_length = 20)
	p_id = models.CharField(max_length = 10,primary_key=True)
	p_name = models.CharField(max_length = 20)  
	p_cost = models.DecimalField(max_digits = 8, decimal_places=1) 
	p_price = models.DecimalField(max_digits = 8, decimal_places=1) 
	p_inventory = models.DecimalField(max_digits = 8, decimal_places=0)
	p_hcost = models.DecimalField(max_digits = 8, decimal_places=1) 
	p_estsupply = models.DecimalField(max_digits = 8, decimal_places=0)
	p_estdemand = models.DecimalField(max_digits = 8, decimal_places=0)
	p_reorder = models.DecimalField(max_digits = 8, decimal_places=0,default=1000)
	def __str__(self):
		return self.p_id



class Order(models.Model):
	o_id = models.CharField(max_length = 30,primary_key=True) # 食物名稱
	o_price = models.DecimalField(max_digits = 8, decimal_places=1)
	o_date = models.DateField(default=date.today)
	c_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
	p_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	o_profit = models.DecimalField(max_digits = 8, decimal_places=0,default=100)
	o_quantity = models.DecimalField(max_digits = 8, decimal_places=0,default=10)

	def __str__(self):
		return self.o_id


class Material(models.Model):
	m_id = models.CharField(max_length = 10,primary_key=True)
	m_name = models.CharField(max_length = 20)
	m_date = models.DateField(default=date.today)
	m_price = models.DecimalField(max_digits = 8, decimal_places=1) 
	m_inventory = models.DecimalField(max_digits = 8, decimal_places=0)# decimal_places=0 不可有小數
	m_hcost = models.DecimalField(max_digits = 8, decimal_places=1,default=0,) 
	m_estsupply = models.DecimalField(max_digits = 8, decimal_places=0, default=0)
	m_estdemand = models.DecimalField(max_digits = 8, decimal_places=0,default=0)
	m_reorder = models.DecimalField(max_digits = 8, decimal_places=0,default=1000)
	def __str__(self):
		return self.m_id



class Consume(models.Model):
	H_quantity = models.DecimalField(max_digits = 8, decimal_places=0) 
	o_id = models.ForeignKey(Order, on_delete=models.CASCADE) 
	p_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Use(models.Model):
	U_quantity = models.DecimalField(max_digits = 8, decimal_places=0) 
	m_id = models.ForeignKey(Material, on_delete=models.CASCADE) 
	p_id = models.ForeignKey(Product, on_delete=models.CASCADE)

class Retention(models.Model):
	Period = models.DecimalField(max_digits = 3, decimal_places=0,primary_key=True) 
	Retention = models.DecimalField(max_digits = 5, decimal_places=1)
	Survival = models.DecimalField(max_digits = 5, decimal_places=1)
	Active_Customers = models.DecimalField(max_digits = 5, decimal_places=1)
	Active_Periods = models.DecimalField(max_digits = 5, decimal_places=1)
	def __int__(self):
		return self.Period

