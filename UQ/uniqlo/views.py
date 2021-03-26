from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer,Product,Order,Material,Consume,Use,Retention
from django.db.models import Avg, Max, Min, Sum, Count
import random
import math
from datetime import date
import datetime
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
from plotly.graph_objs import Pie
from django.db.models import F
# from django.db.models import F
def home(request):

	return render(request,'home.html', locals())

def raw_plot(request):
	allproduct = Material.objects.values('m_id').distinct()
	YS = Material.objects.all().filter(m_id = post_id(request)).values('m_estdemand')
	mat_id =post_id(request)
	YearS = list(YS)
	try: 
		daydemand = YearS[0]['m_estdemand']
	except IndexError:
		daydemand = 0
	n = int(daydemand)

	supply = Material.objects.all().filter(m_id = post_id(request)).values('m_estsupply')
	sup = list(supply)
	try: 
		daysupply = sup[0]['m_estsupply']
	except IndexError:
		daysupply = 0
	s = int(daysupply)

	inventory = Material.objects.all().filter(m_id = post_id(request)).values('m_inventory')
	inventory = list(inventory)
	try: 
		inventory = inventory[0]['m_inventory']
	except IndexError:
		inventory = 0
	
	m = int(inventory)
	#假設每三個期間再訂購一次 estdemand*3=estsupply
	x_data = [n,2*n,3*n-s,4*n-s,5*n-s,6*n-2*s,7*n-2*s,8*n-2*s,9*n-3*s,10*n-3*s,11*n-3*s,12*n-4*s,13*n-4*s,14*n-4*s,15*n-5*s,16*n-5*s,]
	y_data = [inventory-x for x in x_data]
	plot_div = plot([Scatter(x=[i for i in range(17)], y=y_data,
					mode='lines', name='inventory',
					opacity=0.8, marker_color='red')],
					output_type='div')
	return render(request,'raw_plot.html', locals())

#選單頁
def index(request):
#計算單月特定產品銷售額占比
	customers = Customer.objects.all()
	orders = Order.objects.all().values('p_id').distinct()

	#n = post_id(request)
	n = year_id(request)
	m = month_id(request)
	year = int(n)
	month = int(m)
	if month==2:
		d1 = datetime.date(year,month,28)
	elif month==4 or 6 or 9 or 11:
		d1 = datetime.date(year,month,30)
	else:
		d1 = datetime.date(year,month,31)
	d = datetime.date(year,month,1)
	#d1 = datetime.date(year,month,28)
#要注意2月只有28天-->exception
	rev=Order.objects.filter(o_date__lte=d1,o_date__gte=d).values('o_price')
	mrev=list(rev)
	revenue=0
	for i in mrev:
		revenue += i['o_price']
	#gte >= ; lte <=

	keyin = post_id(request)
	ppp=Order.objects.filter(o_date__lte=d1,o_date__gte=d,p_id=post_id(request)).values('o_price')
	pp=ppp[:]
	pp=ppp[:]
	see=list(pp)
	ttotal=0
	for i in see:
		ttotal += i['o_price']
	a = int(ttotal)
	b = int(revenue)
	try:
		percent = 100*a/b
	except ZeroDivisionError:
		percent = 0
	zara = random.randint(5,22)
	hm = random.randint(2,14)
	l=[]
	l.append('others')
	l.append('ZARA')
	l.append('H&M')
	l.append('Uniqlo')
	value=[]
	value.append(100-percent-zara-hm)
	value.append(zara)
	value.append(hm)
	value.append(percent)
	plot_div = plot([Pie(labels=l, values=value)],output_type='div')
	#cuscount = Customer.objects.order_by('c_id').filter(c_id__range=[107306000,107306005]).values('c_fdate')
	return render(request, 'index.html', locals())

def customer(request):
	n = year_id(request)
	m = month_id(request)
	year = int(n)
	month = int(m)
	if month==2:
		d1 = datetime.date(year,month,28)
	elif month==4 or 6 or 9 or 11:
		d1 = datetime.date(year,month,30)
	else:
		d1 = datetime.date(year,month,31)
	d = datetime.date(year,month,1)
	customers = Customer.objects.all().filter(c_fdate__lte=d1,c_fdate__gte=d).order_by('c_id')
	context = {"customers":customers}
	return render(request, 'customer.html', context)

def cus_retention(request):
	n = (datetime.datetime.now()-datetime.timedelta(days=15)).strftime("%Y-%m-%d")
	retent = Retention.objects.all().order_by('Period')
	ret = Retention.objects.all().order_by('Period').values('Active_Periods')
	
	#values 取欄位名稱
	orderlist = list(ret)
	total = 0
	for i in orderlist:
		total += i['Active_Periods']
	sumall = int(total)
	r_period = sumall/8000
	return render(request, 'retention.html', locals())

def month_id(request):
	try:
		x=request.POST['m_id']
	except KeyError:
		x='1'
	return x

def year_id(request):
	try:
		x=request.POST['y_id']
	except KeyError:
		x='2020'
	return x

def post_id(request):
	try:
		x = request.POST['filt_id']
	except KeyError:
		x = '001'
	return x

def sel_id(request):
	#select_id = request.POST['select_pid']
	try:
		x = request.POST['select_pid']
	except KeyError:
		x = '001'
	return x
#銷售部門頁面呈現
def sales(request):
#計算單月特定產品利潤占比
# 	allproduct = Order.objects.values('p_id').distinct()
# #條列id
# 	n = (datetime.datetime.now()-datetime.timedelta(days=30)).strftime("%Y-%m-%d")
# 	#日期回推至n天前
# 	var = Order.objects.all().values('o_price')
# 	#values 取欄位名稱
# 	summary = var[:]
# 	orderlist = list(summary)
# 	# QUERYSET轉LIST
# 	total = 0
# 	for i in orderlist:
# 		total += i['o_price']
# 		#逐項加總
# 	day = Customer.objects.all().filter(c_fdate__lte = n).values('c_fdate')
# 	daylist = day[:]
# 	date = list(daylist)
# 	fdate = []
# 	for n in date:
# 		fdate.append(n)
# 		#逐項印出日期
# 	times = Order.objects.all().filter(c_id = post_id(request)).count()
	#使用者在網頁輸入要查詢的id 網頁呈現查詢結果
	customers = Customer.objects.all()
	orders = Order.objects.all().values('p_id').distinct()
	#n = post_id(request)
	n = year_id(request)
	m = month_id(request)
	year = int(n)
	month = int(m)
	d = datetime.date(year,month,1)
	if month==2:
		d1 = datetime.date(year,month,28)
	elif month==4 or 6 or 9 or 11:
		d1 = datetime.date(year,month,30)
	else:
		d1 = datetime.date(year,month,31)
#要注意2月只有28天-->exception
	rev=Order.objects.filter(o_date__lte=d1,o_date__gte=d).values('o_profit')
	mrev=list(rev)
	revenue=0
	for i in mrev:
		revenue += i['o_profit']
	#gte >= ; lte <=
	# ppp=Order.objects.filter(o_date__lte=d1,o_date__gte=d,p_id='005').values('o_price')
	ppp=Order.objects.filter(o_date__lte=d1,o_date__gte=d,p_id=post_id(request)).values('o_profit')
	pp=ppp[:]
	pp=ppp[:]
	see=list(pp)
	ttotal=0
	for i in see:
		ttotal += i['o_profit']

	a = int(ttotal)
	b = int(revenue)
	try:
		percent = 100*a/b
	except ZeroDivisionError:
		percent = 0

	l=[]
	l.append('others')
	l.append(post_id(request))
	value=[]
	value.append(100-percent)
	value.append(percent)
	
	plot_div = plot([Pie(labels=l, values=value)],output_type='div')
	return render(request, 'sales.html', locals())





def marketing(request):
#request.POST.get('select_pid')
#算歷年單一產品總品類佔有率
	allorder = Order.objects.values('p_id').distinct()
	rev = Order.objects.all().filter(p_id=sel_id(request)).values('o_quantity')
	return_id = str(sel_id(request))
	#values 取欄位名稱
	orderlist = list(rev)
	total = 0
	for i in orderlist:
		total += i['o_quantity']
				#逐項加總
	category_sales = float(total)

	full = random.randint(1000, 1200)
	proportion = 100*category_sales / full
	proportion = round(proportion,4)
	zara = random.randint(9,28)
	hm = random.randint(7,14)
	l=[]
	l.append('others')
	l.append('ZARA')
	l.append('H&M')
	# l.append(sel_id(request))
	l.append('Uniqlo')
	value=[]
	
	value.append(100-proportion-zara-hm)
	value.append(zara)
	value.append(hm)
	value.append(proportion)
	plot_div = plot([Pie(labels=l, values=value)],output_type='div')
	#假設該品類銷售總量 100000
	return render(request, 'marketing.html', locals())

# def dropdownMenu(request):
# 	allorder = Order.objects.values('p_id').distinct()
# 	return render(request, "profit.html", locals())

def Profit(request):
	p = Order.objects.all().filter(p_id = post_id(request)).values('o_profit')
	order = list(p)
	total = 0
	for i in order:
		total += i['o_profit']
	Category_Profit = float(total)

	p0 = Order.objects.all().values('o_profit')
	order0 = list(p0)
	total1 = 0
	for i in order0:
		total1 += i['o_profit']
	Total_Profit = float(total1)
	proportion = 100*Category_Profit/Total_Profit
	per = Category_Profit/Total_Profit
	l=[]
	l.append('other products')
	l.append(post_id(request))
	value=[]
	
	value.append(1-per)
	value.append(per)
	plot_div = plot([Pie(labels=l, values=value)],output_type='div')

#下拉選單
	allp = Order.objects.values('p_id').distinct()
	return render(request, 'profit.html', locals())

def EPQ_calculate(request):
	low = Product.objects.all().order_by('p_inventory')
	YP = Product.objects.all().filter(p_id = post_id(request)).values('p_estdemand')
	theid = post_id(request)
	YearP = list(YP)
	Dtotal = 0
	for i in YearP:
		Dtotal += i['p_estdemand']
	Dday = float(Dtotal)
	Y_Production = Dday * 250
#250為每年生產天數

	S = Product.objects.all().filter(p_id = post_id(request)).values('p_estsupply')
	YearS = list(S)
	Stotal = 0
	for i in YearS:
		Stotal += i['p_estsupply']
	Sday = float(Stotal)

	HC = Product.objects.all().filter(p_id = post_id(request)).values('p_hcost')
	H = list(HC)
	H_Cost = 0
	for i in H:
		H_Cost += i['p_hcost']
	Holding = float(H_Cost)
	#100為生產準備費用
	e =  (2*Y_Production*100) 
	p = Holding *(1-(Dday/Sday))
	Q = e/p
	C_EPQ = math.sqrt(Q)
	C_EPQ = round(C_EPQ,4)
	# EPQ_DB = EPQ.objects.create(EPQ = C_EPQ) 
	# EPQ_DB.save()
	allproduct = Product.objects.values('p_id').distinct()
	return render(request, 'production.html', locals())

def Raw_EOQ(request):
	# low = Material.objects.all().filter(m_inventory__lte=1500)
	low = Material.objects.all().order_by('m_inventory')
	YS = Material.objects.all().filter(m_id = post_id(request)).values('m_estdemand')
	theid = post_id(request)
	YearS = list(YS)
	Stotal = 0
	for i in YearS:
		Stotal += i['m_estdemand']
	Sday = float(Stotal)
	Y_Sales = Sday * 300
#300*為每年販售天數*日銷
	OC = Material.objects.all().filter(m_id = post_id(request)).values('m_price')
	O = list(OC)
	Order_Cost = 0
	for i in O:
		Order_Cost += i['m_price']
	Ordercost = float(Order_Cost)
#訂購成本
	HC = Material.objects.all().filter(m_id = post_id(request)).values('m_hcost')
	H = list(HC)
	H_Cost = 0
	for i in H:
		H_Cost += i['m_hcost']
	Holding = float(H_Cost)
	#100為生產準備費用
	e =  (2*Y_Sales*Ordercost) 
	p = Holding
	
	try:
		Q = e/p
	except ZeroDivisionError:
		Q = 0
	C_EOQ = math.sqrt(Q)
	C_EOQ = round(C_EOQ,0)
	int(C_EOQ)
#product list 選單
	allproduct = Material.objects.values('m_id').distinct()

#更新EOQ置資料庫
	inventory = Material.objects.filter(m_id = post_id(request)).values('m_inventory')
	inv = list(inventory)
	left = 0
	for i in inv:
		left += i['m_inventory']
	products_in = int(left)
	new = products_in + C_EOQ
	Material.objects.filter(m_id = post_id(request)).update(m_inventory = new)
	Material.objects.filter(m_id = post_id(request)).update(m_date = datetime.datetime.now())
	# Material.objects.filter(m_id = post_id(request)).update(m_date = datetime.datetime.now()+datetime.timedelta(days=15))
	reorder = Material.objects.filter(m_id = post_id(request)).values('m_estdemand')

	re = list(reorder)
	r = 0
	for i in re:
		r += i['m_estdemand']
	d_demand = int(r)
	days = random.randint(15, 20)
	re_point = d_demand * days + 750
	Material.objects.filter(m_id = post_id(request)).update(m_reorder = re_point)
	return render(request, 'material.html', locals())

def cal_inventory(request):#更新inventory
	#Cons = Order.objects.all().aggregate(Max('o_id'))
	Cons = Order.objects.filter(p_id = post_id(request)).order_by('-o_id').values()[0]
#抓出最新的order資料 並從inventory中減掉
	#Cons = Order.objects.filter(p_id = post_id(request)).order_by('-o_date')[0]
	Cons = str(Cons)
	x = Cons.find("'o_quantity': Decimal")
	inv = Cons[x:]
	minus = inv.split('\'')[3]
	Consumes = int(minus)
	#total = 0
	# for i in C:
	# 	total += i['o_quantity']
	#Consumes = int(total)

	invent = Product.objects.filter(p_id = post_id(request)).values('p_inventory')
	inv = list(invent)
	left = 0
	for i in inv:
		left += i['p_inventory']
	inventory = int(left)
	#Consumes = 0
	new = inventory - Consumes
	Product.objects.filter(p_id=post_id(request)).update(p_inventory = new)
	orders = Order.objects.values('p_id').distinct()
	allorder = Order.objects.all().order_by('-o_date')
	return render(request, 'update.html', locals())


def EOQ_calculate(request):
	low = Product.objects.all().order_by('p_inventory')
	YS = Product.objects.all().filter(p_id = post_id(request)).values('p_estdemand')
	theid = post_id(request)
	YearS = list(YS)
	Stotal = 0
	for i in YearS:
		Stotal += i['p_estdemand']
	Sday = float(Stotal)
	Y_Sales = Sday * 300
#300*為每年販售天數*日銷
	OC = Product.objects.all().filter(p_id = post_id(request)).values('p_cost')
	O = list(OC)
	Order_Cost = 0
	for i in O:
		Order_Cost += i['p_cost']
	Ordercost = float(Order_Cost)
#訂購成本
	HC = Product.objects.all().filter(p_id = post_id(request)).values('p_hcost')
	H = list(HC)
	H_Cost = 0
	for i in H:
		H_Cost += i['p_hcost']
	Holding = float(H_Cost)
	#100為生產準備費用
	e =  (2*Y_Sales*Ordercost) 
	p = Holding
	#Q = e/p
	try:
		Q = e/p
	except ZeroDivisionError:
		Q = 0
	C_EOQ = math.sqrt(Q)
	C_EOQ = round(C_EOQ,0)
	int(C_EOQ)
#product list 選單
	allproduct = Product.objects.values('p_id').distinct()

#更新EOQ置資料庫
	inventory = Product.objects.filter(p_id = post_id(request)).values('p_inventory')
	inv = list(inventory)
	left = 0
	for i in inv:
		left += i['p_inventory']
	products_in = int(left)
	new = products_in + C_EOQ
	Product.objects.filter(p_id = post_id(request)).update(p_inventory = new)

	reorder = Product.objects.filter(p_id = post_id(request)).values('p_estdemand')
	re = list(reorder)
	r = 0
	for i in re:
		r += i['p_estdemand']
	d_demand = int(r)
	days = random.randint(15, 20)
	re_point = d_demand * days + 750
	Product.objects.filter(p_id = post_id(request)).update(p_reorder = re_point)
	return render(request, 'order.html', locals())




def c_rfm(request):
	w=int(month_id(request))*4
	#timedela doesn't have months attribute, so i use weeks
	n = (datetime.datetime.now()-datetime.timedelta(weeks=w)).strftime("%Y-%m-%d")
	#day = Customer.objects.all().filter(c_fdate__lte = n).values('c_fdate')
	day = Customer.objects.all().order_by('-c_fdate').filter(c_fdate__lte = n).values('c_fdate')
	daylist=day[:]
	daylist=list(daylist)

	money=0
	buytimes=0
	d_list=[]
	frequency=0
	avg_cost=0.0
	for i in daylist:
		#等於0這邊都是歸零，讓跑下一個list數值都清空
		buytimes=0
		frequency=0
		avg_cost=0.0
		money=0
		i=i['c_fdate']
		lost_customer=Customer.objects.all().filter(c_fdate=i).values('c_name')
		clist=list(lost_customer)

		for n in clist:
			n=n['c_name']
			find_cid=Customer.objects.all().filter(c_name=n).values('c_id')
			ff=list(find_cid)
			for x in ff:
				x=x['c_id']
				cost=Order.objects.all().filter(c_id=x).values('o_price')
				cc=list(cost)
				for t in cc:
					t=t['o_price']
					money=money+t
					buytimes=buytimes+1
				try:
					round(money,2)
					avg_cost=money/buytimes
					avg_cost=round(avg_cost,2)
				except ZeroDivisionError:
					avg_cost=0
				# avg_cost=money/buytimes
				try:
					frequency=1/buytimes
					frequency=round(frequency,2)
				except ZeroDivisionError:
					frequency=0
				#frequency=1/buytimes
				d_list.append({'Name':n,'Recurrency':i,'Frequency':frequency,'Money':avg_cost})
	return render(request,'rfm.html',locals())
