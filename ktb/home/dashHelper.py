from home.models import *
import datetime
# from datetime import date
from django.contrib import messages

def QtyIn():
	records=SaveInventory.objects.all()
	qtyin=0.0
	for i in records:
		qtyin=qtyin+i.qtyin

	return qtyin

def QtyOut():
	records=SaveInventory.objects.all()
	qtyout=0.0
	for i in records:
		qtyout=qtyout+i.qtyout

	return qtyout

def Incoming():
	records=PaymentAndFinance.objects.all()
	incoming=0.0
	for i in records:
		incoming=incoming

	return incoming

def Outgoing():
	records=PaymentAndFinance.objects.all()
	outgoing=0.0
	for i in records:
		outgoing=outgoing
	return outgoing

def Receiveable1():
	print("in rec 1")
	payment=0.0
	
	record=PaymentAndFinance.objects.all()
	for i in record:
		if i.trn.types=='Sales':

			if i.dueDate != 'NA':
				due=datetime.datetime.strptime(i.dueDate,"%d/%m/%Y").date()
				if due<datetime.date.today():
					if i.balanceDue>0:
						payment=payment+i.balanceDue
						print(payment)
	return payment

def Receiveable2():
	print("in rec2")
	payment=0.0
	record=PrePayments.objects.all()
	for i in record:
		if i.trn.types=='Sales':
			balance=i.advance-i.advanceFromBuyers
			if i.dueDate != 'NA':
				print(i.dueDate)
				due=datetime.datetime.strptime(i.dueDate,"%Y-%m-%d").date()
				print(due)
				if due<datetime.date.today() and balance>0:
					payment=payment+(i.advance-i.advanceFromBuyers)
	return payment
#due=datetime.strptime(i.dueDate,'%Y-%m-%d').date()
def Payable1():
	print("pay 1")
	payment=0.0
	record=PaymentAndFinance.objects.all()
	for i in record:
		if i.trn.types=='Purchase':
			if i.dueDate != 'NA':
				due=datetime.datetime.strptime(i.dueDate,"%d/%m/%Y").date()
				if due<datetime.date.today() and i.balanceDue>0:
					payment=payment+i.balanceDue
					print(payment)
	return payment

def Payable2():
	payment=0.0
	record=PrePayments.objects.all()
	for i in record:
		if i.trn.types=='Purchase':
			balance=i.advance-i.advanceToSellers
			if i.dueDate != 'NA':
				due=datetime.datetime.strptime(i.dueDate,"%d/%m/%Y").date()
				if due<datetime.date.today() and balance>0:
					payment=payment+(i.advance-i.advanceToSellers)
					print(payment)
	return payment

def Profit():
	records=PL.objects.all()
	profit=0.0
	for i in records:
		if i.grossProfit>=0:
			profit=profit+i.grossProfit
		

	return profit

def Loss():
	records=PL.objects.all()
	loss=0.0
	for i in records:
		if i.grossProfit<0:
			loss=loss+i.grossProfit

	return loss

def Finance():
	try:
		obj=PaymentAndFinance.objects.all()
		for i in obj:
			if i.buyerDueDate < datetime.today():
				messages.info(request, 'Due date for sales payment'+i.trn.s_trn)

			if i.supplierDueDate < datetime.today():
				messages.info(request, 'Due date for purchase payment'+i.trn.p_trn)

			if i.s_logisticsPaymentDue < datetime.today():
				messages.info(request, 'Due date for sales logistics payment'+i.trn.p_trn)

			if i.p_logisticsPaymentDue < datetime.today():
				messages.info(request, 'Due date for purchase logistics payment'+i.trn.p_trn)
	except:
		obj=None

	return obj

	