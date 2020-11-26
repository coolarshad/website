from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from home.models import *
from login.models import *
import costmanagement.models as cost
import calendar
from datetime import timedelta 
from datetime import datetime
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.urls import reverse
from home.templatetags import custom_tags
from django.shortcuts import redirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from login import *
from django.contrib import messages
from home import dashHelper
from home.logs import *
from django.contrib.auth.hashers import make_password
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login

# @csrf_exempt
# user=None
def UserLogin(request):
	try:
		username=request.POST['user']
		password=request.POST['password']
		user = authenticate(name=username, password=password)
		login(request,user)
		Logging(request,'Signed In')
		return redirect('home:index')
	except Exception as e:
		print(e)
		return redirect('login')
@login_required
def Index(request):
	# print(request.POST['test'])
	try:
	
		# unapproved=TradeApproval.objects.filter(Q(trade_status='')).count()
		try:
			if TradeApproval.objects.filter(Q(trade_status='Approved')).exists():
				approved=TradeApproval.objects.filter(Q(trade_status='Approved')).count()
			else:
				approved=0
			#print(approved)

			if TradeApproval.objects.filter(Q(trade_status='')).exists():
				unapproved=TradeApproval.objects.filter(Q(trade_status='')).count()
			
			else:
				unapproved=0
			#print(unapproved)	

			

			pending=[]
			if SalesAndPurchase.objects.all().exists():
				t=TradeApproval.objects.all()
				for i in t:
				# print(i.trn)
					if SalesAndPurchase.objects.filter(trn__trn=i.trn).exists():
						pass
					else:
						pending.append(i)
				# print(pending)
				balanceinventory=len(pending)#SaveInventory.objects.latest('inventoryvalue').inventoryvalue
			else:
				balanceinventory=0
			#print(balanceinventory)

			if TradeApproval.objects.filter(Q(trade_status='Approved',types='Sales')).exists():
				salesproduct=TradeApproval.objects.filter(Q(trade_status='Approved',types='Sales'))
			else:
				salesproduct=None
			#print(salesproduct)

			if TradeApproval.objects.filter(Q(trade_status='Approved',types='Purchase')).exists():
				purchaseproduct=TradeApproval.objects.filter(Q(trade_status='Approved',types='Purchase'))
			else:
				purchaseproduct=None
			# print(purchaseproduct)

			if SalesAndPurchase.objects.all().exists():
				salesandpurchase=SalesAndPurchase.objects.all()
			else:
				salesandpurchase=None
			#print(salesandpurchase)

			if ExtraCost.objects.all().exists():
				extras=ExtraCost.objects.all()
			else:
				extras=None
			# print(str(extras)+"extra")
			

			if PL.objects.all().exists():
				pl=PL.objects.all()
				# bill=SalesAndPurchase.objects.all()
			else:
				pl=None
			#print(pl)

			if PaymentAndFinance.objects.all().exists():
				payf=PaymentAndFinance.objects.all()
				
			else:
				payf=None
			#print(payf)

			if PrePayments.objects.all().exists():
				prepay=PrePayments.objects.all()
				pre=[]
				for i in prepay:
		# if i.trn.types=='Sales':
					if i.dueDate != 'NA':
						if i.trn.types == 'Sales':
							remaining=i.advance-i.advanceFromBuyers
						if i.trn.types == 'Purchase':
							remaining=i.advance-i.advanceToSellers

						due=datetime.strptime(i.dueDate,'%Y-%m-%d').date()
			# if due<date.today():
						if remaining != 0:
							pre.append(i)
				
				inventory_product,inventory_qty=GetInventory()
				# print(inventory_qty)
		

			messages.success(request,'Entered into Home Page.')
			# print('11')
			return render(request,"index.html",{'balanceinventory':balanceinventory,'approved':approved,'unapproved':unapproved,
				'payf':payf,'prepay':pre,'pl':pl,'extras':extras,'sales':salesandpurchase,'salesproduct':salesproduct,'purchaseproduct':purchaseproduct,'inventory_product':zip(inventory_product,inventory_qty)})
			
		except:
			return render(request,"index.html")
	except Exception as e:
		print(e)
		return redirect('login')
	# return render(request,"index.html")


def GetInventory():
	# sp=[]
	# pro=[]
	showinventoryqtys=[]
	showinventoryproduct=[]
	products=[]
	qtys=[]

	products=TradeApproval.objects.order_by().values_list('baseproduct',flat=True).distinct().order_by('baseproduct')
	for i in products:#reading names with redundancy
		# sp.append('break')#for new line
		sps=SalesAndPurchase.objects.filter(trn__baseproduct__exact=i)#all trns with name i
		if sps.count() != 0:#if not empty
			# pro.append(i)#add for display
			val=0
			for j in sps:#each element from i
				# sp.append(j)
				if j.trn.types != 'Cancel Purchase' and j.trn.types != 'Cancel Sales':
			# val=val+row.billQty
					if j.trn.types == 'Purchase':
						val=val+j.billQty
						# products.append(i)
						qtys.append(val)
					if j.trn.types == 'Sales':
						val=val-j.billQty
						# products.append(i)
						qtys.append(val)
			showinventoryqtys.append(qtys[-1])
			showinventoryproduct.append(i)

	return showinventoryproduct,showinventoryqtys



@login_required
def Dashboard(request):
	return redirect('home:index')

@login_required
def Users(request):
	try:
		obj=User.objects.all()
		
	except ObjectDoesNotExist:
		obj=None

	cxt={'users':obj}
	return render(request,'usermanagement.html',context=cxt)

@login_required
def SaveUsers(request):
	try:
		password=request.POST['user-management_password-input']
		password=make_password(password)
		obj=User.objects.create(name=request.POST['user-management_name-input'],position=request.POST['user-management_position-input'],authority=request.POST['user-management_authority-input'],
			contact=request.POST['user-management_contact-input'],email=request.POST['user-management_email-input'],password=password)
		obj.save()
		print('user registered')
		
		Logging(request,'User created '+obj.name)
		
	except Exception as e:
		print(e)

	return redirect('home:users')
@login_required
def EditUsers(request):
	try:
		password=request.POST['user-management_password-input']
		password=make_password(password)
		obj=User.objects.filter(name=request.POST['user-management_name-input']).update(position=request.POST['user-management_position-input'],authority=request.POST['user-management_authority-input'],
			contact=request.POST['user-management_contact-input'],email=request.POST['user-management_email-input'],password=password)
		# obj.save()
		print('user updated')
		
		Logging(request,'User Updated/Edited '+obj.name)
		

	except Exception as e:
		print(e)

	return redirect('home:users')

@login_required
def KycData(request):
	try:
		records=Kyc.objects.all().order_by('name')
	except Exception as e:
		print(e)
	return render(request,'kyc.html',{'records':records})

@login_required
def TradeApprove(request):
	# print('in view')
	try:
		sn=SnCount.objects.latest('sn')
		sn=sn.sn
		sn=sn+1
	except:
		sn=1
	try:
		kpref=TradeRefNo.objects.latest('kp')
		kpref=kpref.kp+1
		print(kpref)
	except:
		kpref=1
	try:	
		ksref=TradeRefNo.objects.latest('sl')
		ksref=ksref.sl+1
		print(ksref)
	except:
		ksref=1

	records=TradeApproval.objects.filter(Q(trade_status='')).order_by('-sn')
	pro=[]
	products=TradeApproval.objects.order_by().values_list('baseproduct',flat=True).distinct().order_by('baseproduct')
	for i in products:
		# sp.append('break')
		sps=SalesAndPurchase.objects.filter(trn__baseproduct__exact=i)
		if sps.count() != 0:
			pro.append(i)
		# for j in sps:
			# sp.append(j)
	# records=TradeApproval.objects.all()
	# print(records)
	companies=Kyc.objects.filter(approve2=True).order_by('name')
	
	cxt={'sn':sn,'kpref':kpref,'ksref':ksref,'records':records,'companies':companies,'products':pro}
	return render(request,'tradeapproval.html',context=cxt)

@login_required
def SaveApproval(request):
	if request.POST['types-input']=='Sales Amendment' or request.POST['types-input']=='Purchase Amendment':
		try:
			trade=TradeApproval.objects.filter(trn=request.POST['traderefno-input']).update(sn=request.POST['number-input'],
			company=request.POST['company-input'],
			types=request.POST['types-input'],product=request.POST['product-input'],origin=request.POST['origin-input'],
			client=request.POST['client-input'],address=request.POST['address-input'],tcq=request.POST['contractqnty-input'],
			contractUnit=request.POST['contractunit-input'],tolerance=request.POST['tolerance-input'],packing=request.POST['packing-input'],
			tuq=request.POST['tradeupdateqnty-input'],tuqUnit=request.POST['contractUnit-input'],contractBalanceQty=request.POST['contractbalanceqnty-input'],
			contractBalanceUnit=request.POST['contractbalanceunit-input'],ratePMT=request.POST['ratepmt-input'],
			commissionAgent=request.POST['commissionagent-input'],commissionRate=request.POST['commissionrate-input'],
			logisticProvider=request.POST['logisticprovider-input'],estimatedLogisticsCost=request.POST['estimatedlogisticcost-input'],
			paymentTerm=request.POST['paymentterm-input'],incoterm=request.POST['incoterm-input'],pod=request.POST['pod-input'],pol=request.POST['pol-input'],
			remarks=request.POST['remark-input'],etd=request.POST['etd-input'],eta=request.POST['eta-input'],trd=request.POST['traderefdate-input'],baseproduct=request.POST['product-name'],
			bank=request.POST['bank-input'],account=request.POST['acountnum-input'],swift=request.POST['swiftcode-input'])
			print('done records saving')

			Logging(request,'Trade Approval request edited for '+ trade.trn)
		except Exception as e:
			print(e)
		return redirect('home:tradeApproval')
	else:
		try:
			# print('inside')
			trade=TradeApproval.objects.create(sn=request.POST['number-input'],
				company=request.POST['company-input'],trd=request.POST['traderefdate-input'],trn=request.POST['traderefno-input'],
				types=request.POST['types-input'],product=request.POST['product-input'],origin=request.POST['origin-input'],
				client=request.POST['client-input'],address=request.POST['address-input'],tcq=request.POST['contractqnty-input'],
				contractUnit=request.POST['contractunit-input'],tolerance=request.POST['tolerance-input'],packing=request.POST['packing-input'],
				tuq=request.POST['tradeupdateqnty-input'],tuqUnit=request.POST['contractUnit-input'],contractBalanceQty=request.POST['contractbalanceqnty-input'],
				contractBalanceUnit=request.POST['contractbalanceunit-input'],ratePMT=request.POST['ratepmt-input'],
				commissionAgent=request.POST['commissionagent-input'],commissionRate=request.POST['commissionrate-input'],
				logisticProvider=request.POST['logisticprovider-input'],estimatedLogisticsCost=request.POST['estimatedlogisticcost-input'],
				paymentTerm=request.POST['paymentterm-input'],incoterm=request.POST['incoterm-input'],pod=request.POST['pod-input'],pol=request.POST['pol-input'],
				etd=request.POST['etd-input'],eta=request.POST['eta-input'],remarks=request.POST['remark-input'],approve1=False,approve2=False,baseproduct=request.POST['product-name'],
				bank=request.POST['bank-input'],account=request.POST['acountnum-input'],swift=request.POST['swiftcode-input'])
			# print('outside')
			trade.save()
			print('done records saving')

			sn=SnCount.objects.create(sn=request.POST['number-input'])
			sn.save()
		# keep track of product in contract
			if request.POST['types-input'] == 'Purchase':
				try:
					if PurchaseProductTrace.objects.filter(product=request.POST['product-input']).exists():
						s=PurchaseProductTrace.objects.filter(product=request.POST['product-input']).update(
						tuq=request.POST['tradeupdateqnty-input'],tbq=request.POST['contractbalanceqnty-input'])
					else:
						s=PurchaseProductTrace.objects.create(product=request.POST['product-input'],
						tcq=request.POST['contractqnty-input'],tuq=request.POST['tradeupdateqnty-input'],
						tbq=request.POST['contractbalanceqnty-input'],first_trn=request.POST['traderefno-input'])
						s.save()
				except Exception as e:
					print(e)
			if request.POST['types-input'] == 'Sales':
				try:
					if SalesProductTrace.objects.filter(product=request.POST['product-input']).exists():
						s=SalesProductTrace.objects.filter(product=request.POST['product-input']).update(
						tuq=request.POST['tradeupdateqnty-input'],tbq=request.POST['contractbalanceqnty-input'])
					else:
						s=SalesProductTrace.objects.create(product=request.POST['product-input'],
							tcq=request.POST['contractqnty-input'],tuq=request.POST['tradeupdateqnty-input'],
							tbq=request.POST['contractbalanceqnty-input'],first_trn=request.POST['traderefno-input'])
						s.save()
				except Exception as e:
					print(e)
			# approve=ApprovedBy.objects.create(trn=trade,approve1=False,approve2=False)
			# approve.save()

			kp_pattern='KP'
			ks_pattern='SL'

			kp=''
			ks=''

			refno=request.POST['traderefno-input']
			print(refno)
			ref=refno[2:].lstrip('0')	
			if refno.startswith(kp_pattern):
			
				# print(ref.lstrip('0'))
				# print(int(ref))
				try:
					x=TradeRefNo.objects.latest('kp')
					x=ref
					y=TradeRefNo.objects.latest('sl')
					y=y.sl
					no=TradeRefNo.objects.create(kp=x,sl=y)
					no.save()
					print('kp')
				except Exception as e:
					no=TradeRefNo.objects.create(kp=1,sl=0)
					no.save()
		
			if refno.startswith(ks_pattern):
				try:
					x=TradeRefNo.objects.latest('kp')
					x=x.kp
					y=TradeRefNo.objects.latest('sl')
					y=ref
					no=TradeRefNo.objects.create(kp=x,sl=y)
					no.save()
				except:
					no=TradeRefNo.objects.create(kp=0,sl=1)
					no.save()
			
				print('created')
				
				Logging(request,'Trade request created '+trade.trn)
			
		except Exception as e:
			print(e)
		return redirect('home:tradeApproval')
@login_required
def TradeApproved(request):
	try:
		records=TradeApproval.objects.filter(Q(trade_status='Approved')).order_by('-sn')
		companies=Kyc.objects.filter(approve2=True).order_by('name')
		pro=[]
		products=TradeApproval.objects.order_by().values_list('baseproduct',flat=True).distinct().order_by('baseproduct')
		for i in products:
		# sp.append('break')
			sps=SalesAndPurchase.objects.filter(trn__baseproduct__exact=i)
			if sps.count() != 0:
				pro.append(i)
	except ObjectDoesNotExist:
		records=None
	return render(request,'tradeapproved.html',{'records':records,'companies':companies,'products':pro})

@csrf_exempt
def GetProductTrace(request):
	product=request.POST['product']
	types=request.POST['types']
	if types == 'Purchase':
		# print('purchase')
		try:
			pro=PurchaseProductTrace.objects.get(product=product)
			balance=pro.tbq-pro.tuq
			data={'product':pro.product,'tcq':pro.tcq,'tuq':pro.tuq,'tbq':balance}
		except:
			pro=None
			data={'product':'','tcq':0,'tuq':0,'tbq':0}

	if types == 'Sales':
		try:
			pro=SalesProductTrace.objects.get(product=product)
			balance=pro.tbq-pro.tuq
			data={'product':pro.product,'tcq':pro.tcq,'tuq':pro.tuq,'tbq':balance}
		except:
			pro=None
			data={'product':'','tcq':0,'tuq':0,'tbq':0}

	return JsonResponse(data)

@csrf_exempt
def GetPieData(request):
	print('chart')
	try:
		profit=0
		loss=0
		obj=PL.objects.all()
		for i in obj:
			if i.grossProfit>0:
				profit=profit+i.grossProfit
				# print(str(profit)+'profit')
			else:
				loss=loss+abs(i.grossProfit)
				# print(str(loss)+'loss')

		cxt={'profit':profit,'loss':loss}
	except Exception as e:
		
		print(e)
		cxt={'profit':0,'loss':0}

	return JsonResponse(cxt)

@login_required
def Prepayments(request):
	try:
		trns=TradeApproval.objects.all().order_by('-sn')
		records=PrePayments.objects.all().order_by('-trn')
	except ObjectDoesNotExist:
		records=None
	return render(request,'prepayments.html',{'trns':trns,'records':records})

@login_required
def SavePayments(request):
	trn=request.POST['pre_trn-input']
	obj=TradeApproval.objects.get(trn=trn)
	if request.POST['tradetype-input']=='Sales':

		try:
			print('pre sales')
			record=PrePayments.objects.create(trn=obj,
			dueDate=request.POST['duedate'],advance=request.POST['advance-input'],lcNumberValue=request.POST['inlcnum-input'],
			lcIssuingBank=request.POST['lcissuingval-input'],advanceFromBuyers=request.POST['advancepayment-input'],
			receivedDate=request.POST['paymentdate-input'],lcExpiryDate=request.POST['lc_expirydate-input'],nextShipmentDate=request.POST['lc_shipmentdate-input'],remarks=request.POST['lc_remarks-input'])

			record.save()
			print('done prepayments')
			Logging(request,'Prepayments filed for '+obj.trn)
		except Exception as e:
			print(e)
	else:
		try:
			print('pre purchase')
			record=PrePayments.objects.create(trn=obj,
			dueDate=request.POST['duedate'],advance=request.POST['advance-input'],lcNumberValue=request.POST['inlcnum-input'],
			lcIssuingBank=request.POST['lcissuingval-input'],advanceToSellers=request.POST['advancepayment-input'],
			paidDate=request.POST['paymentdate-input'],lcExpiryDate=request.POST['lc_expirydate-input'],nextShipmentDate=request.POST['lc_shipmentdate-input'],remarks=request.POST['lc_remarks-input'])

			record.save()
			print('done prepayments')

			
			Logging(request,'Prepayments filed for '+obj.trn)
			
		except Exception as e:
			print(e)

	return redirect('home:prepayments')

@login_required		
def PreDocuments(request):
	try:
		records=TradeApproval.objects.all().order_by('-trn')

	except ObjectDoesNotExist:
		records=None
	return render(request,'presale.html',{'records':records})


@login_required
def SalesPurchase(request):
	try:
		trns=PrePayments.objects.all().order_by('-trn')
		records=SalesAndPurchase.objects.all().order_by('-trn')

	except ObjectDoesNotExist:
		records=None
	return render(request,'salespurchase.html',{'trns':trns,'records':records})
@login_required
def SaveSalesPurchase(request):
	trn=request.POST['traderefno']
	obj=TradeApproval.objects.get(trn=trn)
	

	try:
		
		record=SalesAndPurchase.objects.create(trn=obj,
			invoiceDate=request.POST['invoicedate-input'],invoiceNumber=request.POST['invoicenumber-input'],
			invoiceAmount=request.POST['invoice_amount-input'],commissionAgent=request.POST['commissionagent-input'],
			commissionAmount=request.POST['commission_amount-input'],packingListDetails=request.POST['packaginglist-input'],
			billNumber=request.POST['blnumber-input'],billQty=request.POST['bl_quantity-input'],
			billDate=request.POST['bldate-input'],logisticAgent=request.POST['logisticagent-input'],
			logisticCost=request.POST['logisticcost-input'],liner=request.POST['liner-input'],
			eta=request.POST['eta-input'],etd=request.POST['etd-input'],shipmentStatus=request.POST['shipmentstatus-input'],remarks=request.POST['salespurchase_remarks-input'])

		record.save()
		print('done salesPurchase')

		Logging(request,'Sales and Purchase filled for '+obj.trn)
		
	except Exception as e:
		print(e)

	return redirect('home:salesPurchase')
@login_required
def ExtraCosts(request):
	try:
		trns=TradeApproval.objects.all().order_by('-trn')
		records=ExtraCost.objects.all().order_by('-trn')
	except ObjectDoesNotExist:
		records=None
	return render(request,'extracost.html',{'trns':trns,'records':records})
@login_required
def SaveExtraCost(request):
	trn=request.POST['traderefno']
	obj=TradeApproval.objects.get(trn=trn)
	

	try:
		
		record=ExtraCost.objects.create(trn=obj,
			bankCharges=request.POST['bankcharges-input'],billFee=request.POST['blfee-input'],
			billCollectionCharges=request.POST['blcollectioncharge-input'],otherCharges=request.POST['othercharges-input'],remarks=request.POST['extracost_remarks-input'])
		record.save()
		print('done extras')
		
		Logging(request,'ExtraCost filled for '+obj.trn)
		
	except Exception as e:
		print(e)
	return redirect('home:extraCost')
@login_required
def PaymentFinance(request):
	try:
		trns=SalesAndPurchase.objects.all().order_by('-trn')
		records=PaymentAndFinance.objects.all().order_by('-trn')
	except ObjectDoesNotExist:
		records=None
	return render(request,'paymentfinance.html',{'trns':trns,'records':records})

@csrf_exempt
def PaymentFinanceHelper(request):
	trn=request.POST['traderef']
	print(trn)
	obj=TradeApproval()
	if TradeApproval.objects.filter(trn=trn).exists():
		obj=TradeApproval.objects.get(trn=trn)
		# print(obj.sn)
	

	sp=SalesAndPurchase.objects.get(trn=obj)
	# print(sp)
	pre=PrePayments.objects.get(trn=obj)
	
	salespurchase=SalesAndPurchase.objects.get(trn=obj)
	print(salespurchase.invoiceAmount)
	# pre calculated values
	if pre.advanceFromBuyers == None:
		pre.advanceFromBuyers=0
	if pre.advanceToSellers == None:
		pre.advanceToSellers=0
		print(pre.advanceToSellers)

	
	tad=datetime.strptime(obj.tad,'%Y-%m-%d').date().strftime('%d/%m/%y')
	# print(obj.tad)
	print(obj.types)
	if obj.types == 'Sales' or obj.types == 'Sales Amendment':

		balancepayment=salespurchase.invoiceAmount-pre.advanceFromBuyers
		print(balancepayment)
	else:
		print('in'+str(pre.advanceToSellers))
		balancepayment=salespurchase.invoiceAmount-pre.advanceToSellers
		print(balancepayment)

	if obj.paymentTerm == '100% against OBL Copy Documents':
		# duedate = tad+timedelta(15)
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')
		# print(duedate)
	if obj.paymentTerm == '10% advance & 90% against OBL Copy Documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == '20% advance & 80% against OBL Copy Documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%m/%d/%y')

	if obj.paymentTerm == '30% advance & 70% against OBL Copy Documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')
		
	if obj.paymentTerm == '60% advance & 40% against OBL Copy Documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == '100% advance against PI':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == 'Sight DLC':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == 'Usance 30 days DLC' or obj.paymentTerm == 'LC 30 DAYS FROM BL DATE':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(30)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == 'Usance 45 days DLC' or obj.paymentTerm == 'LC 45 DAYS FROM BL DATE':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(45)
		duedate=datetime.strftime(duedate,'%d/%m/%y')
	
	if obj.paymentTerm == 'Usance 60 days DLC' or obj.paymentTerm == 'LC 60 DAYS FROM BL DATE':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(60)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == 'Usance 90 days DLC' or obj.paymentTerm == 'LC 90 DAYS FROM BL DATE':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(90)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == 'DAP 100%':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == '20% advance & 80% DAP':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == '7 days after OBL date upon clean documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(7)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == '10 days after OBL date upon clean documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(10)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == '15 days after OBL date upon clean documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(15)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == '30 days after OBL date upon clean documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(30)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	if obj.paymentTerm == '60 days after OBL date upon clean documents':
		duedate = datetime.strptime(tad,'%d/%m/%y').date()+timedelta(60)
		duedate=datetime.strftime(duedate,'%d/%m/%y')

	logisticsandcommissionduedate=datetime.strptime(salespurchase.billDate,'%d/%m/%Y')+timedelta(15)
	logisticsandcommissionduedate=datetime.strftime(logisticsandcommissionduedate,'%d/%m/%y')
	
	logisticsdue=salespurchase.logisticCost
	agentcommissiondue=salespurchase.commissionAmount

	pack={'types':obj.types,'balancepayment':balancepayment,'duedate':duedate,'logisticprovider':obj.logisticProvider,
	'commissionagent':obj.commissionAgent,'logisticsdue':logisticsdue,'agentcommissiondue':agentcommissiondue,
	'logisticsandcommissionduedate':logisticsandcommissionduedate,'client':obj.client}
		
	return JsonResponse(pack)
	# return redirect(reverse('home:paymentFinance'),custom_tags.SP(obj))

@csrf_exempt
def PrepaymentsHelper(request):
	trn=request.POST['trn']

	print(trn+' pre pay')
	try:
		obj=TradeApproval.objects.get(trn=trn)
		try:
			# doc=Documents.objects.get(trn=obj)
			# print(doc.po_date+timedelta(8))
			# print(doc.po_date)
			if obj.types == 'Sales' or obj.types == 'Sales Amendment':
				adv=float(obj.tuq)*float(obj.ratePMT)
				s_duedate=datetime.strptime(obj.so_date,'%Y-%m-%d').date()+timedelta(7)
				# print('in sales'+str(s_duedate))
				cxt={
				'types':obj.types,
				'incoterm':obj.incoterm,
				'trn':obj.trn,
				'paymentTerm':obj.paymentTerm,
				'incoterm':obj.incoterm,
				'duedate':s_duedate,
				'total':adv,
				'client':obj.client,
				}

			if obj.types == 'Purchase' or obj.types == 'Purchase Amendment':
				adv=float(obj.tuq)*float(obj.ratePMT)
				p_duedate=datetime.strptime(obj.po_date,'%Y-%m-%d').date()+timedelta(7)
				# print('in sales'+str(p_duedate))
				cxt={
				'types':obj.types,
				'incoterm':obj.incoterm,
				'trn':obj.trn,
				'paymentTerm':obj.paymentTerm,
				'incoterm':obj.incoterm,
				'duedate':p_duedate,
				'total':adv,
				'client':obj.client,
				}
		except Exception as e:
			print(e)
			doc=None
	except Exception as e:
		print(e)
		obj=None

	return JsonResponse(cxt)

@csrf_exempt
def SalesPurchaseHelper(request):
	trn=request.POST['traderef']
	obj=TradeApproval()
	if TradeApproval.objects.filter(trn=trn).exists():
		obj=TradeApproval.objects.get(trn=trn)
	else:
		obj=None
	# try:
	# 	doc=Documents.objects.get(trn=obj)
	# except Exception as e:
	# 	print(e)
	# pre calculated values
	invoiceamount=(float(obj.tuq)*float(obj.ratePMT))
	commissionamount=float(obj.commissionRate)*float(obj.tuq)

	if obj.types == 'Sales' or obj.types == 'Sales Amendment':
		pack={'types':'Sales','invoicedate':obj.so_date,'invoicenumber':obj.so_number,'invoiceamount':invoiceamount,'commissionagent':obj.commissionAgent,
		'commissionamount':commissionamount,'packaginglist':obj.packing,'blnumber':obj.so_number,'billqty':obj.tuq,
		'bldate':obj.so_date,'logisticagent':obj.logisticProvider,'logisticcost':obj.estimatedLogisticsCost,'tolerance':obj.tolerance,
		'ratePMT':float(obj.ratePMT),'commissionRate':float(obj.commissionRate),'client':obj.client,'baseproduct':obj.baseproduct}
	else:
		pack={'types':'Purchase','invoicedate':obj.po_date,'invoicenumber':obj.po_number,'invoiceamount':invoiceamount,'commissionagent':obj.commissionAgent,
		'commissionamount':commissionamount,'packaginglist':obj.packing,'blnumber':obj.po_number,'billqty':obj.tuq,
		'bldate':obj.po_date,'logisticagent':obj.logisticProvider,'logisticcost':obj.estimatedLogisticsCost,'tolerance':obj.tolerance,
		'ratePMT':float(obj.ratePMT),'commissionRate':float(obj.commissionRate),'client':obj.client,'baseproduct':obj.baseproduct}
	# return redirect(reverse('home:salesPurchase'),custom_tags.ObjectData(obj))
	return JsonResponse(pack)
@login_required
def SaveFinance(request):
	trn=request.POST['traderefno']
	obj=TradeApproval.objects.get(trn=trn)
	print(obj)
	try:
		print('entered')
		record=PaymentAndFinance.objects.create(trn=obj,
			balancePayment=request.POST['balancepayment-input'],dueDate=request.POST['paymentduedate-input'],
			payment=request.POST['payment-input'],paymentDate=request.POST['paymentdate-input'],
			balanceDue=request.POST['balancedue-input'],paymentMode=request.POST['paymentmode-input'],
			paymentStatus=request.POST['statusofpayments-input'],logisticsPaymentDue=request.POST['logisticpaymenttobepaid-input'],
			logisticsProvider=request.POST['logisticagent-input'],commissionAgent=request.POST['comissionagent-input'],
			logisticsCommissionDueDate=request.POST['duedate_logistic_comissions-input'],
			agentCommissionDueDate=request.POST['duedate_agent_comissions-input'],
			agentCommissionPaid=request.POST['agent_commissionamountpaid-input'],
			remarks=request.POST['salespurchase_remarks-input'])
			
		record.save()
		print('done extras')

		
		Logging(request,'Payment and Finance filled for '+obj.trn)
		
	except Exception as e:
		print(e)
	return redirect('home:paymentFinance')

def Dispute(request):
	try:
		trns=TradeApproval.objects.all()
		records=Disputes.objects.all()
	except ObjectDoesNotExist:
		records=None
	return render(request,'dispute.html',{'trns':trns,'records':records})

def SaveDisputes(request):
	sn=request.POST['traderefno']
	obj=TradeApproval()
	if TradeApproval.objects.filter(s_trn=sn).exists():
		obj=TradeApproval.objects.get(s_trn=sn)
		print(obj.sn)
	else:
		obj=TradeApproval.objects.get(p_trn=sn)
		print(obj.sn)


	try:
		print('entered')
		record=Disputes.objects.create(trn=obj,
			s_dispute=request.POST['salesdispute-input'],
			p_dispute=request.POST['purchasedispute-input'],
			s_remark=request.POST['salesremarks-input'],
			p_remark=request.POST['purchaseremarks-input'])
		record.save()
		print('disputes done')

	except Exception as e:
		print(e)

	return redirect('home:disputes')

@login_required
def PLBook(request):
	try:
		trn=[]
		sps=[]
		trns=PaymentAndFinance.objects.all().order_by('-trn')
		
		records=PL.objects.all().order_by('-trn')
		for i in records:
			t=TradeApproval.objects.get(trn=i.p_trn)
			tr=TradeApproval.objects.get(trn=i.trn)
			if SalesAndPurchase.objects.filter(trn=tr).exists():
				sp=SalesAndPurchase.objects.get(trn=tr)
				sps.append(sp.invoiceDate)
				# print(sp.invoiceDate)
			else:
				sps.append(None)
			trn.append(t)
		print(sps)
	except ObjectDoesNotExist:
		records=None
	return render(request,'psl.html',{'records':zip(records,sps),'trns':trns,'trn':trn,'sps':sps})

@csrf_exempt
def EditPL(request):
	trn=request.POST['trn']
	remarks=request.POST['remarks']
	print('editing'+str(trn))
	pl=PL.objects.filter(trn__trn__exact=trn).update(remarks=remarks)
	Logging(request,'PL edited for '+str(trn))
	return redirect('home:pl')

@login_required
def SavePLBook(request):
	purchase=request.POST['purchaseref']
	sales=request.POST['salesref']
	
	try:
		saleObj=TradeApproval.objects.get(trn=sales)
	except:
		saleObj=None

	try:
		purchaseObj=TradeApproval.objects.get(trn=purchase)
	except:
		purchaseObj=None

	# try:
	sale_obj=SalesAndPurchase.objects.get(trn=saleObj)
		# print(str(sale_obj.commissionAmount)+"in obj")
	# sales_extra=ExtraCost.objects.get(trn=saleObj)
	if ExtraCost.objects.filter(trn=saleObj).exists():
		sales_extra=ExtraCost.objects.get(trn=saleObj)
		s_bankCharges=sales_extra.bankCharges
		s_billFee=sales_extra.billFee
		s_billCollectionCharges=sales_extra.billCollectionCharges
		s_otherCharges=sales_extra.otherCharges
	else:
		s_bankCharges=0
		s_billFee=0
		s_billCollectionCharges=0
		s_otherCharges=0
	
	# except:
		# sale_obj=None
		# sales_extra=None

	# try:
	purchase_obj=SalesAndPurchase.objects.get(trn=purchaseObj)
		
	if ExtraCost.objects.filter(trn=purchaseObj).exists():
		purchase_extra=ExtraCost.objects.get(trn=purchaseObj)
		p_bankCharges=purchase_extra.bankCharges
		p_billFee=purchase_extra.billFee
		p_billCollectionCharges=purchase_extra.billCollectionCharges
		p_otherCharges=purchase_extra.otherCharges
	else:
		p_bankCharges=0
		p_billFee=0
		p_billCollectionCharges=0
		p_otherCharges=0

		# p_ptc=purchase_obj.invoiceAmount+purchase_obj.commissionAmount+purchase_obj.logisticCost+purchase_extra.bankCharges+purchase_extra.billFee+purchase_extra.billCollectionCharges+purchase_extra.otherCharges
		# print(purchase_extra)
	# except:
	# 	purchase_obj=None
	# 	purchase_extra=None

	# print(sale_obj.trn)
	s_ptc=sale_obj.commissionAmount+sale_obj.logisticCost+s_bankCharges+s_billFee+s_billCollectionCharges+s_otherCharges
	p_ptc=purchase_obj.invoiceAmount+purchase_obj.commissionAmount+purchase_obj.logisticCost+p_bankCharges+p_billFee+p_billCollectionCharges+p_otherCharges

	trfs=sale_obj.invoiceAmount
	gp=trfs-(p_ptc+s_ptc)
	ppd=gp/sale_obj.billQty
	try:
		pl=PL.objects.create(trn=saleObj,p_trn=purchase,s_purchaseTotalCost=s_ptc,p_purchaseTotalCost=p_ptc,totalRevenueFromSales=trfs,grossProfit=gp,profitPerDrum=ppd,remarks=request.POST['profitloss-input'])
		pl.save()
		print('done pl: '+pl.p_trn)

		
		Logging(request,'PL book saved for '+pl.trn.trn)
		
	except Exception as e:
		print(e)
	return redirect('home:pl')

@login_required
def Inventory(request):
	
	sp=[]
	pro=[]
	products=TradeApproval.objects.order_by().values_list('baseproduct',flat=True).distinct().order_by('baseproduct')
	for i in products:
		sp.append('break')
		sps=SalesAndPurchase.objects.filter(trn__baseproduct__exact=i)
		if sps.count() != 0:
			pro.append(i)
		for j in sps:
			sp.append(j)
		

	return render(request,'inventory.html',{'trades':sp,'products':pro})
@login_required
def SaveInventoryRecord(request):
	
	obj=SaveInventory.objects.create(sn=request.POST['sn_inventory-input'],
		entrydate=request.POST['entrydate-input'],godowndate=request.POST['dodowndate-input'],
		trn=request.POST['ta_ref_no-input'],product=request.POST['product-input'],trd=request.POST['refdate-input'],supplier=request.POST['supplier-input'],
		qtyin=request.POST['qntyindrum-input'],qtyout=request.POST['qntyoutdrum-input'],incoterm=request.POST['cfr-input'],
		expense=request.POST['expenses_incurred-input'],net=request.POST['netprice_drum-input'],
		oldbalqtyvalue=request.POST['oldbalanceqnty-input'],
		balanceqty=request.POST['balanceqnty-input'],unit=request.POST['unit1-input'],
		godownlocation=request.POST['godown_location-input'],oldinventoryvalue=request.POST['oldinventoryvalue-input'],inventoryvalue=request.POST['inventory_value-input'],
		currentinventoryrate=request.POST['inventory_rate-input'])
	obj.save()
	print('inventory saved')
	sn=InventorySn.objects.create(sn=request.POST['sn_inventory-input'])
	sn.save()
	print('sn saved')
	if not Products.objects.filter(name=request.POST['product-input']).exists():
		product=Products.objects.create(name=request.POST['product-input'],balanceqty=request.POST['balanceqnty-input'],inventoryvalue=request.POST['inventory_value-input'],
			unit=request.POST['unit1-input'],inventoryrate=request.POST['inventory_rate-input'])
		product.save()
		print('product saved')
	else:
		Products.objects.filter(name=request.POST['product-input']).update(
			balanceqty=request.POST['balanceqnty-input'],inventoryvalue=request.POST['inventory_value-input'],
			unit=request.POST['unit1-input'],inventoryrate=request.POST['inventory_rate-input'])
		print('product updated')
	
	Logging(request,'Inventory registered for '+obj.trn)
	
	return redirect('home:inventory')

def Stock(request):
	try:
		sn=SnStock.objects.latest('sn')
		sn=sn.sn
		sn=sn+1
	except:
		sn=1

	raws=[]
	additives=[]
	packings=[]
	consumptions=[]

	try:
		obj=StockJournal.objects.all()
		# raws=StockRaw.objects.all()
		# additives=StockAdditive.objects.all()
		# packings=StockPacking.objects.all()
		# consumptions=StockConsumption.objects.all()

		inv=cost.Inventory.objects.all()

		for i in obj:
			raw=i.stockraw_set.all()
			raws.append(raw)
			additive=i.stockadditive_set.all()
			additives.append(additive)
			packing=i.stockpacking_set.all()
			packings.append(packing)
			consumption=i.stockconsumption_set.all()
			consumptions.append(consumption)
	except ObjectDoesNotExist:
		obj=None
		inv=cost.Inventory.objects.all()


	return render(request,'stockjournal.html',{'stocks':zip(obj,raws,additives,packings,consumptions),'sn':sn,'inventory':inv})
def SaveStock(request):
	print("saving "+request.POST['production_product-input'])
	countraw=request.POST['countraw']
	countadditive=request.POST['countadditive']
	countpacking=request.POST['countpacking']
	countblending=request.POST['countblending']
	print(countraw)
	print(countadditive)
	print(countpacking)
	print(countblending)

	try:
		obj=StockJournal.objects.create(stockno=request.POST['stockjournal_num-input'],
			stockdate=request.POST['stockjournal_date-input'],
			product=request.POST['production_product-input'],qty=request.POST['production_quantity-input'],
			unit=request.POST['production_unit-input'],value=request.POST['production_val-input'],
			rate=request.POST['production_rate_per__unit-input'],production_remarks=request.POST['production_remarks-input'],
			consumption_remarks=request.POST['consumptionblockremarks'])
		obj.save()

		for i in range(1,int(countraw)+1):
			print(i)
			try:
				raw=StockRaw.objects.create(product=obj,
					name=request.POST['consumptionproductraw-input'+str(i)],
					qtykg=request.POST['consumptionquantityraw-input'+str(i)],
					density=request.POST['consumptionquantitydensityraw-input'+str(i)],
					qtyliter=request.POST['consumptionquantityliterraw-input'+str(i)],
					ratekg=request.POST['consumptionquantityratekgraw-input'+str(i)],
					valuekg=request.POST['consumptionquantityvaluekgraw-input'+str(i)],
					rateliter=request.POST['consumptionquantityrateliter-input'+str(i)],
					valueliter=request.POST['consumptionquantityvalueliterraw-input'+str(i)])
				raw.save()
			except Exception as e:
				print(e)

		for i in range(1,int(countadditive)+1):
			print(i)
			try:
				raw=StockAdditive.objects.create(product=obj,
					name=request.POST['consumptionproductadditive-input'+str(i)],
					qtykg=request.POST['consumptionquantityadditive-input'+str(i)],
					density=request.POST['consumptionquantitydensityadditive-input'+str(i)],
					qtyliter=request.POST['consumptionquantityliteradditive-input'+str(i)],
					ratekg=request.POST['consumptionquantityratekgadditive-input'+str(i)],
					valuekg=request.POST['consumptionquantityvaluekgadditive-input'+str(i)],
					rateliter=request.POST['consumptionquantityrateliteradditive-input'+str(i)],
					valueliter=request.POST['consumptionquantityvalueliteradditive-input'+str(i)])
				raw.save()
			except Exception as e:
				print(e)

		for i in range(1,int(countpacking)+1):
			print(i)
			try:
				raw=StockPacking.objects.create(product=obj,
					name=request.POST['consumptionproductpacking-input'+str(i)],
					qty=request.POST['consumptionquantitypacking-input'+str(i)],
					unit=request.POST['consumptionunitpacking-input'+str(i)],
					rate=request.POST['consumptionquantityratepacking-input'+str(i)],
					value=request.POST['consumptionquantityvaluepacking-input'+str(i)])
				raw.save()
			except Exception as e:
				print(e)


		for i in range(1,int(countblending)+1):
			print(i)
			try:
				raw=StockConsumption.objects.create(product=obj,
					name=request.POST['consumptionproductblending-input'+str(i)],
					qty=request.POST['consumptionquantityblending-input'+str(i)],
					unit=request.POST['consumptionunitblending-input'+str(i)],
					rate=request.POST['consumptionquantityrateblending-input'+str(i)],
					value=request.POST['consumptionquantityvalueblending-input'+str(i)])
				raw.save()
			except Exception as e:
				print(e)

		sn=SnStock.objects.create(sn=request.POST['stockjournal_num-input'])
		sn.save()
		print('saved sn')
		


		Logging(request,'Stock Journal made for '+request.POST['production_product-input'])
		
	except Exception as e:
		print(e)
	return redirect('home:stocks')

@csrf_exempt
def DeleteStockJournal(request):
	product=request.POST['product']
	print(product)
	stock=StockJournal.objects.get(product=product)
	stock.delete()

	return redirect('home:stocks')

@csrf_exempt
def GetStockProduct(request):
	raws=[]
	additives=[]
	packings=[]
	consumptions=[]

	product=request.POST['product']
	pro=StockJournal.objects.get(product=product)
	raw=pro.stockraw_set.all()
	additive=pro.stockadditive_set.all()
	packing=pro.stockpacking_set.all()
	consumption=pro.stockconsumption_set.all()

	pro=model_to_dict(pro)
	for i in raw:
		raws.append(model_to_dict(i))
	for i in additive:
		additives.append(model_to_dict(i))
	for i in packing:
		packings.append(model_to_dict(i))
	for i in consumption:
		consumptions.append(model_to_dict(i))

		
	return JsonResponse({'product':pro,'raws':raws,'additives':additives,
		'packings':packings,'consumptions':consumptions})




@csrf_exempt
def ExtrasHelper(request):

	trn=request.POST['trn']
	print('in extras helper '+trn)
	try:
		obj=TradeApproval.objects.get(trn=trn)
		# print('in')
		# e=ExtraCost.objects.get(trn=obj)
		# print('out')
		if obj.types == 'Sales' or obj.types == 'Sales Amendment':
			cxt={'types':'Sales','client':obj.client}
		if obj.types == 'Purchase' or obj.types == 'Purchase Amendment':
			cxt={'types':'Purchase','client':obj.client}
	except Exception as e:
		print(e)
		
	return JsonResponse(cxt)

@csrf_exempt
def Approve(request):
	print('in approval'+' '+request.POST['trn'])
	obj=TradeApproval.objects.get(trn=request.POST['trn'])
	print(str(obj)+'approving')
	try:
	# doc=Documents.objects.create(trn=obj)
		person=request.POST['id']

		if person == 'manager1':
			# approve=ApprovedBy.objects.get(trn=obj)
			obj.approve1=True
			obj.manager1=request.POST['manager1']
			obj.approve1date=date.today()
			obj.save()
			
			Logging(request,'manager1 approved for '+obj.trn)
		
			return redirect('home:tradeApproval')
		if person == 'manager2':
			
			try:#create documents
				# doc=Documents.objects.create(trn=obj)
				if obj.types=='Sales':
					obj.so_number=obj.company+'/'+obj.trn
					print(obj.company+'/'+obj.trn)
					obj.so_date=date.today()   #datetime.datetime.now().strftime("%Y-%m-%d")
				if obj.types=='Purchase':
					obj.po_number=obj.trn
					obj.po_date=date.today()
				obj.save()
				print('doc saved')
				# mark approval for filtering
				obj.trade_status='Approved'
		
				obj.tad=date.today()
				print('updating')
				# obj=TradeApproval.objects.get(trn=request.POST['trn']).update(trade_status='Approved',tad=datetime.datetime.today())
				obj.save()
				
				Logging(request,'manager2 approved for '+obj.trn)
				


			except Exception as e:
				print(e)
			

			return redirect('home:tradeApproval')
		
	except Exception as e:
		print(e)
	

	# obj.save()
	return redirect('home:tradeApproval')
	# return redirect(reverse('home:tradeApprove'),custom_tags.ObjectData(record))

@login_required
def SaveKyc(request):
	try:
		obj=Kyc.objects.create(date=request.POST['kyc_company_date-input'],name=request.POST['kyc_company_name-input'],companyRegNo=request.POST['kyc_company_registrationnum_date-input'],
	 		regAddress=request.POST['kyc_company_registered_address-input'],mailingAddress=request.POST['kyc_company_other_address-input'],telephone=request.POST['kyc_company_telephone-input'],
	 		fax=request.POST['kyc_company_fax-input'],person1=request.POST['kyc_company_concernedperson_one-input'],designation1=request.POST['kyc_company_concernedperson_one_designation-input'],mobile1=request.POST['kyc_company_concernedperson_one_mobile-input'],
	 		email1=request.POST['kyc_company_concernedperson_one_email-input'],person2=request.POST['kyc_company_concernedperson_two-input'],
	 		designation2=request.POST['kyc_company_concernedperson_two_designation-input'],
	 		mobile2=request.POST['kyc_company_concernedperson_two_mobile-input'],email2=request.POST['kyc_company_concernedperson_two_email-input'],
	 		banker=request.POST['kyc_company_bankername-input'],address=request.POST['kyc_company_bankeraddress-input'],
	 		swiftCode=request.POST['kyc_company_bankerswiftcode-input'],accountNumber=request.POST['kyc_company_bankersaccountnumber-input'])
		obj.save()
		print('kyc done')
		
		Logging(request,'Kyc created for'+obj.name)
		
	except Exception as e:
	 	print(e)
	return redirect('home:kyc')

@login_required
def LogFile(request):
	try:
		obj=Log.objects.all().order_by('-logdate')
	except Exception as e:
		obj=None
		print(e)
	return render(request,'logfile.html',{'logs':obj})

@login_required
def EditKyc(request):
	try:
		obj=Kyc.objects.filter(name=request.POST['kyc_company_name-input']).update(date=request.POST['kyc_company_date-input'],companyRegNo=request.POST['kyc_company_registrationnum_date-input'],
	 		regAddress=request.POST['kyc_company_registered_address-input'],mailingAddress=request.POST['kyc_company_other_address-input'],telephone=request.POST['kyc_company_telephone-input'],
	 		fax=request.POST['kyc_company_fax-input'],person1=request.POST['kyc_company_concernedperson_one-input'],designation1=request.POST['kyc_company_concernedperson_one_designation-input'],mobile1=request.POST['kyc_company_concernedperson_one_mobile-input'],
	 		email1=request.POST['kyc_company_concernedperson_one_email-input'],person2=request.POST['kyc_company_concernedperson_two-input'],
	 		designation2=request.POST['kyc_company_concernedperson_two_designation-input'],
	 		mobile2=request.POST['kyc_company_concernedperson_two_mobile-input'],email2=request.POST['kyc_company_concernedperson_two_email-input'],
	 		banker=request.POST['kyc_company_bankername-input'],address=request.POST['kyc_company_bankeraddress-input'],
	 		swiftCode=request.POST['kyc_company_bankerswiftcode-input'],accountNumber=request.POST['kyc_company_bankersaccountnumber-input'])
		# obj.save()

		
		Logging(request,'Kyc edited  for'+obj.name)
		
		print('kyc Edit')
	except Exception as e:
	 	print(e)
	return redirect('home:kyc')

@csrf_exempt
def AlterKyc(request):
	company=request.POST['name']
	try:
	 	name=Kyc.objects.get(name=company)
	 	print(name.address)
	 	print(name.swiftCode)
	 	data={'date':name.date,'comp':name.name,'companyRegNo':name.companyRegNo,'regAddress':name.regAddress,
	 	'mailingAddress':name.mailingAddress,'telephone':name.telephone,'fax':name.fax,'person1':name.person1,
	 	'designation1':name.designation1,'mobile1':name.mobile1,'email1':name.email1,'person2':name.person2,
	 	'designation2':name.designation2,'mobile2':name.mobile2,'email2':name.email2,'banker':name.banker,
	 	'address':name.address,'swiftCode':name.swiftCode,'accountNumber':name.accountNumber}
	 	print('kyc done')
	except Exception as e:
	 	print(e)
	return JsonResponse(data)

@csrf_exempt
def AlterUser(request):
	name=request.POST['name']
	print(name)
	try:
	 	name=User.objects.get(name=name)
	 	data={'name1':name.name,'position':name.position,'authority':name.authority,'contact':name.contact,
	 	'email':name.email,'password':name.password}

	 	print('kyc done')
	except Exception as e:
	 	print(e)
	return JsonResponse(data)

@csrf_exempt
def DelKyc(request):
	comp=request.POST['name']
	print(comp)
	try:
		k=Kyc.objects.filter(name=comp).delete()

		
		Logging(name,'KYC deleted '+comp)
		
	except Exception as e:
		print(e)
	return redirect('home:kyc')

@csrf_exempt
def DelUser(request):
	name=request.POST['name']
	print(name)
	try:
		k=User.objects.filter(name=name).delete()
		print('deleted')
		
		Logging(request,'User deleted '+name)
		

	except Exception as e:
		print(e)
	return redirect('home:users')

@csrf_exempt
def FetchCompany(request):
	
	obj=Kyc.objects.get(name=request.POST['name'])
	val={'address':obj.regAddress}
	
	return JsonResponse(val)

@csrf_exempt
def GetDataSales(request):
	trn=request.POST['trn']
	obj=TradeApproval()
	if TradeApproval.objects.filter(trn=trn).exists():
		obj=TradeApproval.objects.get(trn=trn)
		print(obj.trn)
	# doc=Documents.objects.get(trn=obj)
	# print(doc.trn)
	data={'so_number':obj.so_number,'so_date':obj.so_date,'client':obj.client,'address':obj.address,'product':obj.baseproduct,
	'tuq':obj.tuq,'unit':obj.contractUnit,'ratePMT':obj.ratePMT,'incoterm':obj.incoterm,'paymentTerm':obj.paymentTerm,
	'tolerance':obj.tolerance,'pol':obj.pol,'pod':obj.pod,'origin':obj.origin,'packing':obj.packing}

	return JsonResponse(data)

@csrf_exempt
def GetDataPurchase(request):
	trn=request.POST['trn']
	obj=TradeApproval()
	if TradeApproval.objects.filter(trn=trn).exists():
		obj=TradeApproval.objects.get(trn=trn)
		print(obj.so_date)
		print(obj.so_number)
		print('in')
	else:
		obj=None
	# doc=Documents.objects.get(trn=obj)
	# print(doc.trn)

	data={'po_number':obj.po_number,'po_date':obj.po_date,'client':obj.client,'address':obj.address,'tolerance':obj.tolerance,
	'product':obj.baseproduct,'tuq':obj.tuq,'unit':obj.contractUnit,'ratePMT':obj.ratePMT,'incoterm':obj.incoterm,
	'paymentTerm':obj.paymentTerm,'pol':obj.pol,'pod':obj.pod,'etd':obj.etd}

	return JsonResponse(data)

@csrf_exempt
def GetDataInventory(request):
	trn=request.POST['trn']
	obj=TradeApproval()
	if TradeApproval.objects.filter(trn=trn,trade_status='Approved').exists():
		obj=TradeApproval.objects.get(trn=trn)
		sp=SalesAndPurchase.objects.get(trn=obj)
		if obj.types == 'Sales' or obj.types == 'Sales Amendment':
			print('yes in')
			try:
				if SaveInventory.objects.filter(product=sp.trn.product).exists():
					inv=Products.objects.get(name=sp.trn.product)
					print('yes exists')

					data={'product':sp.trn.product,'trd':sp.trn.trd,'client':sp.trn.client,
					'qtyin':0,'qtyout':sp.billQty,'cfr':float(sp.invoiceAmount),'types':obj.types,
					'oldinventoryvalue':inv.inventoryvalue,'oldbalqtyvalue':inv.balanceqty}
				else:
					print('nope')
					data={'product':sp.trn.product,'trd':sp.trn.trd,'client':sp.trn.client,
					'qtyin':0,'qtyout':sp.billQty,'cfr':float(sp.invoiceAmount),'types':obj.types,
					'oldinventoryvalue':0,'oldbalqtyvalue':0}

			except:
				pl=None
				
		

		if obj.types == 'Purchase' or obj.types == 'Purchase Amendment':
			try:
				pl=PL.objects.get(p_trn=obj)
				if SaveInventory.objects.filter(product=sp.trn.product).exists():
					print('yes exists')
					inv=Products.objects.get(name=sp.trn.product)

					print(inv.inventoryvalue)

					data={'product':sp.trn.product,'trd':sp.trn.trd,'client':sp.trn.client,
					'qtyin':sp.billQty,'qtyout':0,'cfr':float(pl.p_purchaseTotalCost),'types':obj.types,
					'oldinventoryvalue':inv.inventoryvalue,'oldbalqtyvalue':inv.balanceqty}
				else:
					print('nope')
					data={'product':sp.trn.product,'trd':sp.trn.trd,'client':sp.trn.client,
					'qtyin':sp.billQty,'qtyout':0,'cfr':float(pl.p_purchaseTotalCost),'types':obj.types,
					'oldinventoryvalue':0,'oldbalqtyvalue':0}
				# s_purchaseTotalCost=pl.s_purchaseTotalCost
			except:
				pl=None
				
			
	return JsonResponse(data)
	
@csrf_exempt
def GetProduct(request):
	product=request.POST['name']
	try:
		inventory=[]
		trns=[]
		obj=SalesAndPurchase.objects.filter(trn__baseproduct__exact=product)
		for i in obj:
			print('new one')
			sp=model_to_dict(i)
			trn=TradeApproval.objects.get(trn=i.trn.trn)
			trn=model_to_dict(trn)
			inventory.append(sp)
			trns.append(trn)
		# print(inventory)
		# print(trn)
		data={'obj':inventory,'trns':trns}
	except ObjectDoesNotExist:
		data={'obj':None,'trns':None}
	

	return JsonResponse(data)
#new ----------------------------------------------
@login_required
def PayableMore(request):
	records=PaymentAndFinance.objects.all()
	finance=[]
	pre=[]
	for i in records:
		# if i.trn.types=='Purchase':
		# if i.dueDate != 'NA':
			# due=datetime.strptime(i.dueDate,'%d/%m/%Y').date()
			# if due<date.today():
		if i.balanceDue != 0.0:
			# print(i.balanceDue)
			pre.append(i)

		# record=PrePayments.objects.all()
	# for i in record:
	# 	if i.trn.types=='Purchase':
	# 		if i.dueDate != 'NA':
	# 			due=datetime.strptime(i.dueDate,'%d/%m/%Y').date()
	# 			if due<date.today():
	# 				balance=i.advance-i.advanceToSellers
	# 				# print(balance)
	# 				if balance>0.0:
	# 					pre.append(i)
	
	return render(request,'payablemore.html',{'payments':pre})
	# return render(request,'payablemore.html',{'payments':records})

@login_required
def ReceivableMore(request):
	# records=PaymentAndFinance.objects.all()
	finance=[]
	pre=[]
	# for i in records:
	# 	if i.trn.types=='Sales':
	# 		if i.dueDate != 'NA':
	# 			due=datetime.strptime(i.dueDate,'%d/%m/%Y').date()
	# 			if due<date.today():
	# 				if i.balanceDue>0.0:
	# 					pre.append(i)

	
	record=PrePayments.objects.all()
	for i in record:
		# if i.trn.types=='Sales':
		if i.dueDate != 'NA':
			if i.trn.types == 'Sales':
				remaining=i.advance-i.advanceFromBuyers
			if i.trn.types == 'Purchase':
				remaining=i.advance-i.advanceToSellers

			due=datetime.strptime(i.dueDate,'%Y-%m-%d').date()
			# if due<date.today():
			if remaining != 0:
				pre.append(i)
				# if i.advance != None and i.advanceToSellers != None:
					# balance=i.advance-i.advanceToSellers
					# if balance>0.0:
						# pre.append(i)
					# balance=i.advance-i.advanceToSellers
					
	
	return render(request,'receivablemore.html',{'payments':pre})



	# -----------------edit parts------------------------------

# @login_required
# def EditTradeApproval(request):
# 	try:
# 		trade=TradeApproval.objects.filter(trn=request.POST['traderefno-input']).update(sn=request.POST['number-input'],
# 			company=request.POST['company-input'],
# 			types=request.POST['types-input'],product=request.POST['product-input'],origin=request.POST['origin-input'],
# 			client=request.POST['client-input'],address=request.POST['address-input'],tcq=request.POST['contractqnty-input'],
# 			contractUnit=request.POST['contractunit-input'],tolerance=request.POST['tolerance-input'],packing=request.POST['packing-input'],
# 			tuq=request.POST['tradeupdateqnty-input'],tuqUnit=request.POST['contractUnit-input'],contractBalanceQty=request.POST['contractbalanceqnty-input'],
# 			contractBalanceUnit=request.POST['contractbalanceunit-input'],ratePMT=request.POST['ratepmt-input'],
# 			commissionAgent=request.POST['commissionagent-input'],commissionRate=request.POST['commissionrate-input'],
# 			logisticProvider=request.POST['logisticprovider-input'],estimatedLogisticsCost=request.POST['estimatedlogisticcost-input'],
# 			paymentTerm=request.POST['paymentterm-input'],incoterm=request.POST['incoterm-input'],pod=request.POST['pod-input'],pol=request.POST['pol-input'],
# 			remarks=request.POST['remark-input'],etd=request.POST['etd-input'],eta=request.POST['eta-input'],trd=request.POST['traderefdate-input'],baseproduct=request.POST['product-name'],
# 			bank=request.POST['bank-input'],account=request.POST['acountnum-input'],swift=request.POST['swiftcode-input'])
# 		print('done records saving')

# 		Logging(request,'Trade Approval request edited for '+ trade)
# 	except Exception as e:
# 		print(e)
# 	return redirect('home:tradeApproval')

@login_required
def EditTradeApproval(request):
	try:
		gdiff=0
		gavailable=0

		trn=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
		if float(trn.tcq) != float(request.POST['contractqnty-input']):
			print('here')
			diff=float(request.POST['contractqnty-input'])-float(trn.tcq)
			if trn.types == 'Sales' or trn.types == 'Sales Amendment':
				pro=SalesProductTrace.objects.get(product=request.POST['product-input'])
				pro.tcq=float(request.POST['contractqnty-input'])
				pro.tbq=float(pro.tbq)+diff
				pro.save()
			if trn.types == 'Purchase' or trn.types == 'Purchase Amendment':
				pro=PurchaseProductTrace.objects.get(product=request.POST['product-input'])
				pro.tcq=float(request.POST['contractqnty-input'])
				pro.tbq=float(pro.tbq)+diff
				pro.save()

		if float(trn.tuq) != float(request.POST['tradeupdateqnty-input']):
			diff=float(request.POST['tradeupdateqnty-input'])-float(trn.tuq)
			gdiff=diff
			if trn.types == 'Sales' or trn.types == 'Sales Amendment':
				pro=SalesProductTrace.objects.get(product=request.POST['product-input'])
				available=float(pro.tbq)-float(pro.tuq)
				gavailable=available
				if diff <= available:
					pro.tbq=float(pro.tbq)-diff
					pro.save()
			if trn.types == 'Purchase' or trn.types == 'Purchase Amendment':
				pro=PurchaseProductTrace.objects.get(product=request.POST['product-input'])
				available=float(pro.tbq)-float(pro.tuq)
				gavailable=available
				if diff <= available:
					pro.tbq=float(pro.tbq)-diff
					pro.save()

		if request.POST['types-input'] == 'Cancel Purchase' or request.POST['types-input'] == 'Cancel Sales':
			print('in cancellation')
			if request.POST['types-input'] == 'Cancel Purchase' and trn.types != 'Cancel Purchase':
				print('in purchse cancel')
				pro=PurchaseProductTrace.objects.get(product=request.POST['product-input'])
				print(pro.tbq)
				pro.tbq=float(pro.tbq)+float(request.POST['tradeupdateqnty-input'])
				print(pro.tbq)
				pro.save()
			if request.POST['types-input'] == 'Cancel Sales' and trn.types != 'Cancel Sales':
				print('in sales cancel')
				pro=SalesProductTrace.objects.get(product=request.POST['product-input'])
				print(pro.tbq)
				pro.tbq=float(pro.tbq)+float(request.POST['tradeupdateqnty-input'])
				print(pro.tbq)
				pro.save()
		
		if TradeApproval.objects.filter(trn=request.POST['traderefno-input']).exists() and gdiff <= gavailable:
			trade=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
			trade.sn=request.POST['number-input']
			trade.company=request.POST['company-input']
			trade.types=request.POST['types-input']
			trade.product=request.POST['product-input']
			trade.origin=request.POST['origin-input']
			trade.client=request.POST['client-input']
			trade.address=request.POST['address-input']
			trade.tcq=request.POST['contractqnty-input']
			trade.contractUnit=request.POST['contractunit-input']
			trade.tolerance=request.POST['tolerance-input']
			trade.packing=request.POST['packing-input']
			trade.tuq=request.POST['tradeupdateqnty-input']
			trade.tuqUnit=request.POST['contractUnit-input']
			trade.contractBalanceQty=request.POST['contractbalanceqnty-input']
			trade.contractBalanceUnit=request.POST['contractbalanceunit-input']
			trade.ratePMT=request.POST['ratepmt-input']
			trade.commissionAgent=request.POST['commissionagent-input']
			trade.commissionRate=request.POST['commissionrate-input']
			trade.logisticProvider=request.POST['logisticprovider-input']
			trade.estimatedLogisticsCost=request.POST['estimatedlogisticcost-input']
			trade.paymentTerm=request.POST['paymentterm-input']
			trade.incoterm=request.POST['incoterm-input']
			trade.pod=request.POST['pod-input']
			trade.pol=request.POST['pol-input']
			trade.remarks=request.POST['remark-input']
			trade.etd=request.POST['etd-input']
			trade.eta=request.POST['eta-input']
			trade.trd=request.POST['traderefdate-input']
			trade.baseproduct=request.POST['product-name']
			trade.bank=request.POST['bank-input']
			trade.account=request.POST['acountnum-input']
			trade.swift=request.POST['swiftcode-input']

			trade.save()
			print('done records saving')
			

			
		Logging(request,'Trade Approval request edited for '+ trade.trn)
	except Exception as e:
		print(e)
	return redirect('home:tradeApproval')

@csrf_exempt
def AlterTradeApproval(request):
	trn=request.POST['trn']
	print(trn)
	try:
		trade=TradeApproval.objects.get(trn=trn)
		if trade.types == 'Sales' or trade.types == 'Sales Amendment' or trade.types == 'Cancel Sales':
			pro=SalesProductTrace.objects.get(product=trade.product)
			first_trn=pro.first_trn
		else:
			pro=PurchaseProductTrace.objects.get(product=trade.product)
			first_trn=pro.first_trn

		# print(trade.trn+'editing')
		data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
		'product':trade.product,'origin':trade.origin,'client':trade.client,'address':trade.address,
		'tcq':trade.tcq,'contractUnit':trade.contractUnit,'tolerance':trade.tolerance,'packing':trade.packing,
		'tuq':trade.tuq,'tuqUnit':trade.tuqUnit,'contractBalanceQty':trade.contractBalanceQty,
		'contractBalanceUnit':trade.contractBalanceUnit,'ratePMT':trade.ratePMT,'commissionAgent':trade.commissionAgent,
		'commissionRate':trade.commissionRate,'logisticProvider':trade.logisticProvider,'estimatedLogisticsCost':trade.estimatedLogisticsCost,
		'paymentTerm':trade.paymentTerm,'incoterm':trade.incoterm,'pol':trade.pol,'pod':trade.pod,
		'etd':trade.etd,'eta':trade.eta,'remarks':trade.remarks,'manager1':trade.manager1,'manager2':trade.manager2,
		'approve1':trade.approve1,'approve2':trade.approve2,'baseproduct':trade.baseproduct,'bank':trade.bank,
		'account':trade.account,'swift':trade.swift,'first_trn':first_trn}

		return JsonResponse(data)
		# print(trade.trn+'editing')
	except Exception as e:
		print(e)

# @login_required
# def EditTradeApproved(request):
# 	try:
# 		obj=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
# 		if request.POST['types-input'] == 'Cancel Sales' or request.POST['types-input'] == 'Cancel Purchase':
			
# 			if not PrePayments.objects.filter(trn=obj):
# 				trade=TradeApproval.objects.filter(trn=request.POST['traderefno-input']).update(sn=request.POST['number-input'],
# 				company=request.POST['company-input'],
# 				types=request.POST['types-input'],product=request.POST['product-input'],origin=request.POST['origin-input'],
# 				client=request.POST['client-input'],address=request.POST['address-input'],tcq=request.POST['contractqnty-input'],
# 				contractUnit=request.POST['contractunit-input'],tolerance=request.POST['tolerance-input'],packing=request.POST['packing-input'],
# 				tuq=request.POST['tradeupdateqnty-input'],tuqUnit=request.POST['contractUnit-input'],contractBalanceQty=request.POST['contractbalanceqnty-input'],
# 				contractBalanceUnit=request.POST['contractbalanceunit-input'],ratePMT=request.POST['ratepmt-input'],
# 				commissionAgent=request.POST['commissionagent-input'],commissionRate=request.POST['commissionrate-input'],
# 				logisticProvider=request.POST['logisticprovider-input'],estimatedLogisticsCost=request.POST['estimatedlogisticcost-input'],
# 				paymentTerm=request.POST['paymentterm-input'],incoterm=request.POST['incoterm-input'],pod=request.POST['pod-input'],pol=request.POST['pol-input'],
# 				remarks=request.POST['remark-input'],etd=request.POST['etd-input'],eta=request.POST['eta-input'],trd=request.POST['traderefdate-input'],baseproduct=request.POST['product-name'],
# 				bank=request.POST['bank-input'],account=request.POST['acountnum-input'],swift=request.POST['swiftcode-input'])
# 			else:
# 				print('not allowed cancel')

# 		if request.POST['types-input'] == 'Sales Amendment' or request.POST['types-input'] == 'Purchase Amendment':
# 		#	if not SalesAndPurchase.objects.filter(trn=obj):
# 			trade=TradeApproval.objects.filter(trn=request.POST['traderefno-input']).update(sn=request.POST['number-input'],
# 				company=request.POST['company-input'],
# 				types=request.POST['types-input'],product=request.POST['product-input'],origin=request.POST['origin-input'],
# 				client=request.POST['client-input'],address=request.POST['address-input'],tcq=request.POST['contractqnty-input'],
# 				contractUnit=request.POST['contractunit-input'],tolerance=request.POST['tolerance-input'],packing=request.POST['packing-input'],
# 				tuq=request.POST['tradeupdateqnty-input'],tuqUnit=request.POST['contractUnit-input'],contractBalanceQty=request.POST['contractbalanceqnty-input'],
# 				contractBalanceUnit=request.POST['contractbalanceunit-input'],ratePMT=request.POST['ratepmt-input'],
# 				commissionAgent=request.POST['commissionagent-input'],commissionRate=request.POST['commissionrate-input'],
# 				logisticProvider=request.POST['logisticprovider-input'],estimatedLogisticsCost=request.POST['estimatedlogisticcost-input'],
# 				paymentTerm=request.POST['paymentterm-input'],incoterm=request.POST['incoterm-input'],pod=request.POST['pod-input'],pol=request.POST['pol-input'],
# 				remarks=request.POST['remark-input'],etd=request.POST['etd-input'],eta=request.POST['eta-input'],trd=request.POST['traderefdate-input'],baseproduct=request.POST['product-name'],
# 				bank=request.POST['bank-input'],account=request.POST['acountnum-input'],swift=request.POST['swiftcode-input'])
# 			#else:
# 			#	print('not allowed Amendment')

# 		if request.POST['types-input'] == 'Sales' or request.POST['types-input'] == 'Purchase':
# 			#if not SalesAndPurchase.objects.filter(trn=obj):
# 			trade=TradeApproval.objects.filter(trn=request.POST['traderefno-input']).update(sn=request.POST['number-input'],
# 				company=request.POST['company-input'],
# 				types=request.POST['types-input'],product=request.POST['product-input'],origin=request.POST['origin-input'],
# 				client=request.POST['client-input'],address=request.POST['address-input'],tcq=request.POST['contractqnty-input'],
# 				contractUnit=request.POST['contractunit-input'],tolerance=request.POST['tolerance-input'],packing=request.POST['packing-input'],
# 				tuq=request.POST['tradeupdateqnty-input'],tuqUnit=request.POST['contractUnit-input'],contractBalanceQty=request.POST['contractbalanceqnty-input'],
# 				contractBalanceUnit=request.POST['contractbalanceunit-input'],ratePMT=request.POST['ratepmt-input'],
# 				commissionAgent=request.POST['commissionagent-input'],commissionRate=request.POST['commissionrate-input'],
# 				logisticProvider=request.POST['logisticprovider-input'],estimatedLogisticsCost=request.POST['estimatedlogisticcost-input'],
# 				paymentTerm=request.POST['paymentterm-input'],incoterm=request.POST['incoterm-input'],pod=request.POST['pod-input'],pol=request.POST['pol-input'],
# 				remarks=request.POST['remark-input'],etd=request.POST['etd-input'],eta=request.POST['eta-input'],trd=request.POST['traderefdate-input'],baseproduct=request.POST['product-name'],
# 				bank=request.POST['bank-input'],account=request.POST['acountnum-input'],swift=request.POST['swiftcode-input'])
# 		#	else:
# 		#		print('not allowed Amendment')
# 		Logging(request,'Trade Approved edited for '+ str(obj))
# 		print('done records saving')
# 	except Exception as e:
# 		print(e)
	
# 	return redirect('home:tradeApproved')
@login_required
def EditTradeApproved(request):
	try:
		obj=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
		if request.POST['types-input'] == 'Cancel Sales' or request.POST['types-input'] == 'Cancel Purchase':
			
			if not PrePayments.objects.filter(trn=obj):
				if request.POST['types-input'] == 'Cancel Purchase' and obj.types != 'Cancel Purchase':
					print('in purchse cancel')
					pro=PurchaseProductTrace.objects.get(product=request.POST['product-input'])
					print(pro.tbq)
					pro.tbq=float(pro.tbq)+float(request.POST['tradeupdateqnty-input'])
					print(pro.tbq)
					pro.save()
				if request.POST['types-input'] == 'Cancel Sales' and obj.types != 'Cancel Sales':
					print('in sales cancel')
					pro=SalesProductTrace.objects.get(product=request.POST['product-input'])
					print(pro.tbq)
					pro.tbq=float(pro.tbq)+float(request.POST['tradeupdateqnty-input'])
					print(pro.tbq)
					pro.save()




				trade=TradeApproval.objects.get(trn=obj.trn)
				trade.sn=request.POST['number-input']
				trade.company=request.POST['company-input']
				trade.types=request.POST['types-input']
				trade.product=request.POST['product-input']
				trade.origin=request.POST['origin-input']
				trade.client=request.POST['client-input']
				trade.address=request.POST['address-input']
				trade.tcq=request.POST['contractqnty-input']
				trade.contractUnit=request.POST['contractunit-input']
				trade.tolerance=request.POST['tolerance-input']
				trade.packing=request.POST['packing-input']
				trade.tuq=request.POST['tradeupdateqnty-input']
				trade.tuqUnit=request.POST['contractUnit-input']
				trade.contractBalanceQty=request.POST['contractbalanceqnty-input']
				trade.contractBalanceUnit=request.POST['contractbalanceunit-input']
				trade.ratePMT=request.POST['ratepmt-input']
				trade.commissionAgent=request.POST['commissionagent-input']
				trade.commissionRate=request.POST['commissionrate-input']
				trade.logisticProvider=request.POST['logisticprovider-input']
				trade.estimatedLogisticsCost=request.POST['estimatedlogisticcost-input']
				trade.paymentTerm=request.POST['paymentterm-input']
				trade.incoterm=request.POST['incoterm-input']
				trade.pod=request.POST['pod-input']
				trade.pol=request.POST['pol-input']
				trade.remarks=request.POST['remark-input']
				trade.etd=request.POST['etd-input']
				trade.eta=request.POST['eta-input']
				trade.trd=request.POST['traderefdate-input']
				trade.baseproduct=request.POST['product-name']
				trade.bank=request.POST['bank-input']
				trade.account=request.POST['acountnum-input']
				trade.swift=request.POST['swiftcode-input']
				trade.save()
				Logging(request,'Trade Approved cancelled for '+ str(obj.trn))
			else:
				print('not allowed cancel')

		if request.POST['types-input'] == 'Sales Amendment' or request.POST['types-input'] == 'Purchase Amendment':
		#	if not SalesAndPurchase.objects.filter(trn=obj):
			

			gdiff=0
			gavailable=0
			trn=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
			if float(trn.tcq) != float(request.POST['contractqnty-input']):
				diff=float(request.POST['contractqnty-input'])-float(trn.tcq)
				if trn.types == 'Sales' or trn.types == 'Sales Amendment':
					pro=SalesProductTrace.objects.get(product=request.POST['product-input'])
					pro.tcq=float(request.POST['contractqnty-input'])
					pro.tbq=float(pro.tbq)+diff
					pro.save()
				if trn.types == 'Purchase' or trn.types == 'Purchase Amendment':
					pro=PurchaseProductTrace.objects.get(product=request.POST['product-input'])
					pro.tcq=float(request.POST['contractqnty-input'])
					pro.tbq=float(pro.tbq)+diff
					pro.save()
					
			if float(trn.tuq) != float(request.POST['tradeupdateqnty-input']):
				diff=float(request.POST['tradeupdateqnty-input'])-float(trn.tuq)
				gdiff=diff
				if trn.types == 'Sales' or trn.types == 'Sales Amendment':
					pro=SalesProductTrace.objects.get(product=request.POST['product-input'])
					available=float(pro.tbq)-float(pro.tuq)
					gavailable=available
					if diff <= available:
						pro.tbq=float(pro.tbq)-diff
						pro.save()
				if trn.types == 'Purchase' or trn.types == 'Purchase Amendment':
					pro=PurchaseProductTrace.objects.get(product=request.POST['product-input'])
					available=float(pro.tbq)-float(pro.tuq)
					gavailable=available
					if diff <= available:
						pro.tbq=float(pro.tbq)-diff
						pro.save()

			

			if TradeApproval.objects.filter(trn=request.POST['traderefno-input']).exists() and gdiff <= gavailable:
				trade=TradeApproval.objects.get(trn=request.POST['traderefno-input'])

				trade.sn=request.POST['number-input']
				trade.company=request.POST['company-input']
				trade.types=request.POST['types-input']
				trade.product=request.POST['product-input']
				trade.origin=request.POST['origin-input']
				trade.client=request.POST['client-input']
				trade.address=request.POST['address-input']
				trade.tcq=request.POST['contractqnty-input']
				trade.contractUnit=request.POST['contractunit-input']
				trade.tolerance=request.POST['tolerance-input']
				trade.packing=request.POST['packing-input']
				trade.tuq=request.POST['tradeupdateqnty-input']
				trade.tuqUnit=request.POST['contractUnit-input']
				trade.contractBalanceQty=request.POST['contractbalanceqnty-input']
				trade.contractBalanceUnit=request.POST['contractbalanceunit-input']
				trade.ratePMT=request.POST['ratepmt-input']
				trade.commissionAgent=request.POST['commissionagent-input']
				trade.commissionRate=request.POST['commissionrate-input']
				trade.logisticProvider=request.POST['logisticprovider-input']
				trade.estimatedLogisticsCost=request.POST['estimatedlogisticcost-input']
				trade.paymentTerm=request.POST['paymentterm-input']
				trade.incoterm=request.POST['incoterm-input']
				trade.pod=request.POST['pod-input']
				trade.pol=request.POST['pol-input']
				trade.remarks=request.POST['remark-input']
				trade.etd=request.POST['etd-input']
				trade.eta=request.POST['eta-input']
				trade.trd=request.POST['traderefdate-input']
				trade.baseproduct=request.POST['product-name']
				trade.bank=request.POST['bank-input']
				trade.account=request.POST['acountnum-input']
				trade.swift=request.POST['swiftcode-input']

				trade.save()

				
			#else:
			#	print('not allowed Amendment')

		if request.POST['types-input'] == 'Sales' or request.POST['types-input'] == 'Purchase':
			#if not SalesAndPurchase.objects.filter(trn=obj):
			

			gdiff=0
			gavailable=0
			trn=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
			if float(trn.tcq) != float(request.POST['contractqnty-input']):
				diff=float(request.POST['contractqnty-input'])-float(trn.tcq)
				if trn.types == 'Sales' or trn.types == 'Sales Amendment':
					pro=SalesProductTrace.objects.get(product=request.POST['product-input'])
					pro.tcq=float(request.POST['contractqnty-input'])
					pro.tbq=float(pro.tbq)+diff
					pro.save()
				if trn.types == 'Purchase' or trn.types == 'Purchase Amendment':
					pro=PurchaseProductTrace.objects.get(product=request.POST['product-input'])
					pro.tcq=float(request.POST['contractqnty-input'])
					pro.tbq=float(pro.tbq)+diff
					pro.save()

			if float(trn.tuq) != float(request.POST['tradeupdateqnty-input']):
				diff=float(request.POST['tradeupdateqnty-input'])-float(trn.tuq)
				gdiff=diff
				if trn.types == 'Sales' or trn.types == 'Sales Amendment':
					pro=SalesProductTrace.objects.get(product=request.POST['product-input'])
					available=float(pro.tbq)-float(pro.tuq)
					gavailable=available
					if diff <= available:
						pro.tbq=float(pro.tbq)-diff
						pro.save()
				if trn.types == 'Purchase' or trn.types == 'Purchase Amendment':
					pro=PurchaseProductTrace.objects.get(product=request.POST['product-input'])
					available=float(pro.tbq)-float(pro.tuq)
					gavailable=available
					if diff <= available:
						pro.tbq=float(pro.tbq)-diff
						pro.save()
			

			if TradeApproval.objects.filter(trn=request.POST['traderefno-input']).exists() and gdiff <= gavailable:
				trade=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
				trade.sn=request.POST['number-input']
				trade.company=request.POST['company-input']
				trade.types=request.POST['types-input']
				trade.product=request.POST['product-input']
				trade.origin=request.POST['origin-input']
				trade.client=request.POST['client-input']
				trade.address=request.POST['address-input']
				trade.tcq=request.POST['contractqnty-input']
				trade.contractUnit=request.POST['contractunit-input']
				trade.tolerance=request.POST['tolerance-input']
				trade.packing=request.POST['packing-input']
				trade.tuq=request.POST['tradeupdateqnty-input']
				trade.tuqUnit=request.POST['contractUnit-input']
				trade.contractBalanceQty=request.POST['contractbalanceqnty-input']
				trade.contractBalanceUnit=request.POST['contractbalanceunit-input']
				trade.ratePMT=request.POST['ratepmt-input']
				trade.commissionAgent=request.POST['commissionagent-input']
				trade.commissionRate=request.POST['commissionrate-input']
				trade.logisticProvider=request.POST['logisticprovider-input']
				trade.estimatedLogisticsCost=request.POST['estimatedlogisticcost-input']
				trade.paymentTerm=request.POST['paymentterm-input']
				trade.incoterm=request.POST['incoterm-input']
				trade.pod=request.POST['pod-input']
				trade.pol=request.POST['pol-input']
				trade.remarks=request.POST['remark-input']
				trade.etd=request.POST['etd-input']
				trade.eta=request.POST['eta-input']
				trade.trd=request.POST['traderefdate-input']
				trade.baseproduct=request.POST['product-name']
				trade.bank=request.POST['bank-input']
				trade.account=request.POST['acountnum-input']
				trade.swift=request.POST['swiftcode-input']
				trade.save()
		#	else:
		#		print('not allowed Amendment')
		Logging(request,'Trade Approved edited for '+ str(obj))
		print('done records saving')
	except Exception as e:
		print(e)
	
	return redirect('home:tradeApproved')

@csrf_exempt
def AlterTradeApproved(request):
	trn=request.POST['trn']
	print('got'+str(trn))
	try:
		trade=TradeApproval.objects.get(trn=trn)
		if trade.types == 'Sales' or trade.types == 'Sales Amendment' or trade.types == 'Cancel Sales':
			pro=SalesProductTrace.objects.get(product=trade.product)
			first_trn=pro.first_trn
		else:
			pro=PurchaseProductTrace.objects.get(product=trade.product)
			first_trn=pro.first_trn

		
		print(trade)
		data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
		'product':trade.product,'origin':trade.origin,'client':trade.client,'address':trade.address,'tad':trade.tad,
		'tcq':trade.tcq,'contractUnit':trade.contractUnit,'tolerance':trade.tolerance,'packing':trade.packing,
		'tuq':trade.tuq,'tuqUnit':trade.tuqUnit,'contractBalanceQty':trade.contractBalanceQty,'trade_status':trade.trade_status,
		'contractBalanceUnit':trade.contractBalanceUnit,'ratePMT':trade.ratePMT,'commissionAgent':trade.commissionAgent,
		'commissionRate':trade.commissionRate,'logisticProvider':trade.logisticProvider,'estimatedLogisticsCost':trade.estimatedLogisticsCost,
		'paymentTerm':trade.paymentTerm,'incoterm':trade.incoterm,'pol':trade.pol,'pod':trade.pod,
		'etd':trade.etd,'eta':trade.eta,'remarks':trade.remarks,'baseproduct':trade.baseproduct,'bank':trade.bank,
		'account':trade.account,'swift':trade.swift,'first_trn':first_trn}

	except Exception as e:
		print(e)
		
	return JsonResponse(data)

@csrf_exempt
def EditDoc(request):
	trn=request.POST['trn']
	print(trn)
	try:
		trade=TradeApproval.objects.get(trn=trn)
		# doc=Documents.objects.get(trn=trade)
		print(trade)

		data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
		'po_number':trade.po_number,'po_date':trade.po_date,'so_number':trade.so_number,'so_date':trade.so_date}
		print(trade.po_number)
	except Exception as e:
		print(e)
	Logging(request,'Documents edited for '+ str(obj))
	return JsonResponse(data)


@login_required
def EditPrePayments(request):
	if request.POST['tradetype-input']=='Sales':

		try:

			trn=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
			obj=PrePayments.objects.filter(trn=trn).update(dueDate=request.POST['duedate'],advance=request.POST['advance-input'],lcNumberValue=request.POST['inlcnum-input'],
			lcIssuingBank=request.POST['lcissuingval-input'],advanceFromBuyers=request.POST['advancepayment-input'],
			receivedDate=request.POST['paymentdate-input'],lcExpiryDate=request.POST['lc_expirydate-input'],nextShipmentDate=request.POST['lc_shipmentdate-input'],remarks=request.POST['lc_remarks-input'])
			# obj.save()
			Logging(request,'prepayments edited for '+ obj.trn)
		except Exception as e:
			print(e)
	else:
		try:

			trn=TradeApproval.objects.get(trn=request.POST['traderefno-input'])
			print(trn)
			obj=PrePayments.objects.filter(trn=trn).update(dueDate=request.POST['duedate'],advance=request.POST['advance-input'],lcNumberValue=request.POST['inlcnum-input'],
			lcIssuingBank=request.POST['lcissuingval-input'],advanceToSellers=request.POST['advancepayment-input'],
			paidDate=request.POST['paymentdate-input'],lcExpiryDate=request.POST['lc_expirydate-input'],nextShipmentDate=request.POST['lc_shipmentdate-input'],remarks=request.POST['lc_remarks-input'])
			# obj.save()
			print(obj.paidDate)
			Logging(request,'prepayments edited for '+ obj.trn)
		except Exception as e:
			print(e)
	
	return redirect('home:prepayments')

@csrf_exempt
def GetSalesBill(request):
	bill=request.POST['bill']
	print(bill)
	try:
		if SalesAndPurchase.objects.filter(trn__types__contains="Purchase",billNumber=bill).exists():
			print('yes')
			obj=SalesAndPurchase.objects.get(trn__types__contains="Purchase",billNumber=bill)
			data={
			'billqty':obj.billQty,
			'liner':obj.liner,
			
			}
		else:
			print('no')
			data={
			'billqty':'',
			'liner':'',
			}
			
	except Exception as e:
		print(e)
			
	return JsonResponse(data)		

@csrf_exempt
def AlterPrePayments(request):
	# print('hello')
	trn=request.POST['trn']
	print(request.POST['trn'])
	try:
		trade=TradeApproval.objects.get(trn=trn)
		pre=PrePayments.objects.get(trn=trade)
		print(trade)

		if trade.types == 'Sales' or trade.types == 'Sales Amendment':
			data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
			'dueDate':pre.dueDate,'advance':pre.advance,'lcNumberValue':pre.lcNumberValue,
			'lcIssuingBank':pre.lcIssuingBank,'advancePay':pre.advanceFromBuyers,
			'Date':pre.receivedDate,'lcExpiryDate':pre.lcExpiryDate,'nextShipmentDate':pre.nextShipmentDate,'incoterm':trade.paymentTerm,'remarks':pre.remarks,'client':trade.client}
		else:
			data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
			'dueDate':pre.dueDate,'advance':pre.advance,'lcNumberValue':pre.lcNumberValue,
			'lcIssuingBank':pre.lcIssuingBank,'advancePay':pre.advanceToSellers,
			'Date':pre.paidDate,'lcExpiryDate':pre.lcExpiryDate,'nextShipmentDate':pre.nextShipmentDate,'incoterm':trade.paymentTerm,'remarks':pre.remarks,'client':trade.client}

		
	except Exception as e:
		print(e)
		
	return JsonResponse(data)

@csrf_exempt
def AlterStock(request):
	# print('hello')
	stockno=request.POST['stockno']
	print(request.POST['stockno'])
	try:
		s=StockJournal.objects.get(stockno=stockno)

		data={'sn':s.sn,'stockno':s.stockno,'stockdate':s.stockdate,
		'c_product1':s.c_product1,'c_qty1':s.c_qty1,'c_unit1':s.c_unit1,'c_altqty1':s.c_altqty1,'c_altunit1':s.c_altunit1,
		'c_product2':s.c_product2,'c_qty2':s.c_qty2,'c_unit2':s.c_unit2,'c_altqty2':s.c_altqty2,'c_altunit2':s.c_altunit2,
		'c_product3':s.c_product3,'c_qty3':s.c_qty3,'c_unit3':s.c_unit3,'c_altqty3':s.c_altqty3,'c_altunit3':s.c_altunit3,
		'p_product':s.p_product,'p_qty':s.p_qty,'p_unit':s.p_unit,'p_altqty':s.p_altqty,'p_altunit':s.p_altunit,
		'warehouse':s.warehouse,'purpose':s.purpose
		}
		
	except Exception as e:
		print(e)
		
	return JsonResponse(data)

@login_required
def EditSalesAndPurchase(request):

	trn=request.POST['traderefno']
	obj=TradeApproval.objects.get(trn=trn)
	

	try:
		print('entered')
		record=SalesAndPurchase.objects.filter(trn=obj).update(invoiceDate=request.POST['invoicedate-input'],invoiceNumber=request.POST['invoicenumber-input'],
			invoiceAmount=request.POST['invoice_amount-input'],commissionAgent=request.POST['commissionagent-input'],
			commissionAmount=request.POST['commission_amount-input'],packingListDetails=request.POST['packaginglist-input'],
			billNumber=request.POST['blnumber-input'],billQty=request.POST['bl_quantity-input'],
			billDate=request.POST['bldate-input'],logisticAgent=request.POST['logisticagent-input'],
			logisticCost=request.POST['logisticcost-input'],liner=request.POST['liner-input'],
			eta=request.POST['eta-input'],etd=request.POST['etd-input'],shipmentStatus=request.POST['shipmentstatus-input'],remarks=request.POST['salespurchase_remarks-input'])

		#record.save()
		print('done SalesPurchase')
	except Exception as e:
		print(e)
	Logging(request,'SalesAndPurchase edited for '+ obj.trn)
	return redirect('home:salesPurchase')

@csrf_exempt
def AlterSalesPurchase(request):
	# print('hello')
	trn=request.POST['trn']
	print(request.POST['trn'])
	try:
		trade=TradeApproval.objects.get(trn=trn)
		sp=SalesAndPurchase.objects.get(trn=trade)
		print(trade)

		data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
			'invoiceDate':sp.invoiceDate,'invoiceNumber':sp.invoiceNumber,'invoiceAmount':sp.invoiceAmount,
			'commissionAgent':sp.commissionAgent,'commissionAmount':sp.commissionAmount,'packingListDetails':sp.packingListDetails,
			'billNumber':sp.billNumber,'billQty':sp.billQty,'billDate':sp.billDate,'logisticAgent':sp.logisticAgent,
			'logisticCost':sp.logisticCost,'liner':sp.liner,'eta':sp.eta,'etd':sp.etd,'shipmentStatus':sp.shipmentStatus,'client':trade.client,'remarks':sp.remarks,'reviewed':sp.reviewed,'baseproduct':trade.baseproduct}
		return JsonResponse(data)
	except Exception as e:
		print(e)
		
	# return JsonResponse(data)


@csrf_exempt
def AlterExtras(request):
	# print('hello')
	trn=request.POST['trn']
	print(request.POST['trn'])
	try:
		trade=TradeApproval.objects.get(trn=trn)
		e=ExtraCost.objects.get(trn=trade)
		print(trade)

		data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
			'bankCharges':e.bankCharges,'billFee':e.billFee,'billCollectionCharges':e.billCollectionCharges,'otherCharges':e.otherCharges,'remarks':e.remarks,'client':trade.client}
		
	except Exception as e:
		print(e)
		
	return JsonResponse(data)

@login_required
def EditExtras(request):

	trn=request.POST['traderefno']
	obj=TradeApproval.objects.get(trn=trn)
	

	try:
		print('entered')
		record=ExtraCost.objects.filter(trn=obj).update(bankCharges=request.POST['bankcharges-input'],billFee=request.POST['blfee-input'],
			billCollectionCharges=request.POST['blcollectioncharge-input'],otherCharges=request.POST['othercharges-input'],remarks=request.POST['extracost_remarks-input'])
		record.save()
		print('done extras')
	except Exception as e:
		print(e)
	Logging(request,'Extras edited for '+ obj.trn)
	return redirect('home:extraCost')


@login_required
def EditPurchaseAndFinance(request):

	trn=request.POST['traderefno']
	obj=TradeApproval.objects.get(trn=trn)
	
	try:
		print('entered')
		record=PaymentAndFinance.objects.filter(trn=obj).update(balancePayment=request.POST['balancepayment-input'],dueDate=request.POST['paymentduedate-input'],
			payment=request.POST['payment-input'],paymentDate=request.POST['paymentdate-input'],
			balanceDue=request.POST['balancedue-input'],paymentMode=request.POST['paymentmode-input'],
			paymentStatus=request.POST['statusofpayments-input'],logisticsPaymentDue=request.POST['logisticpaymenttobepaid-input'],
			logisticsProvider=request.POST['logisticagent-input'],commissionAgent=request.POST['comissionagent-input'],
			logisticsCommissionDueDate=request.POST['duedate_logistic_comissions-input'],
			agentCommissionDueDate=request.POST['duedate_agent_comissions-input'],
			agentCommissionPaid=request.POST['agent_commissionamountpaid-input'],
			remarks=request.POST['salespurchase_remarks-input'])
			
		record.save()
		print('done extras')
	except Exception as e:
		print(e)
	Logging(request,'Purchase and Finance edited for '+ obj.trn)
	return redirect('home:paymentFinance')

@csrf_exempt
def AlterFinance(request):
	# print('hello')
	trn=request.POST['trn']
	print(request.POST['trn'])
	try:
		trade=TradeApproval.objects.get(trn=trn)
		f=PaymentAndFinance.objects.get(trn=trade)
		print(trade)

		data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
			'balancePayment':f.balancePayment,'dueDate':f.dueDate,'payment':f.payment,
			'paymentDate':f.paymentDate,'balanceDue':f.balanceDue,'paymentMode':f.paymentMode,
			'paymentStatus':f.paymentStatus,'logisticsPaymentDue':f.logisticsPaymentDue,
			'logisticsProvider':f.logisticsProvider,'commissionAgent':f.commissionAgent,
			'logisticsCommissionDueDate':f.logisticsCommissionDueDate,'agentCommissionDueDate':f.agentCommissionDueDate,'agentCommissionPaid':f.agentCommissionPaid,'remarks':f.remarks,'client':trade.client}
		
	except Exception as e:
		print(e)
		
	return JsonResponse(data)


@csrf_exempt
def AlterPL(request):
	# print('hello')
	trn=request.POST['trn']
	print(request.POST['trn'])
	try:
		trade=TradeApproval.objects.get(trn=trn)
		p=PL.objects.get(trn=trade)
		seller=TradeApproval.objects.get(trn=p.p_trn)
		sp=SalesAndPurchase.objects.get(trn=trade)
		# buyer=TradeApproval.objects.get(trn=p.trn.trn)
		print(sp.invoiceDate)

		data={'sn':p.trn.sn,'p_trn':p.p_trn,'company':p.trn.company,'trd':p.trn.trd,'trn':p.trn.trn,'types':p.trn.types,
		's_purchaseTotalCost':p.s_purchaseTotalCost,'p_purchaseTotalCost':p.p_purchaseTotalCost,
		'totalRevenueFromSales':p.totalRevenueFromSales,'grossProfit':p.grossProfit,'profitPerDrum':p.profitPerDrum,
		'seller':seller.client,'buyer':p.trn.client,'remarks':p.remarks,'baseproduct':p.trn.baseproduct,'tuq':sp.billQty,'unit':p.trn.tuqUnit,'invoicedate':sp.invoiceDate}
		
	except Exception as e:
		print(e)
		
	return JsonResponse(data)

@csrf_exempt
def EditDisputes(request):

	type=request.POST['id']
	if type=='sales':
		print('yes sales')
		try:
			trn=TradeApproval.objects.get(s_trn=request.POST['trn'])
			obj=Disputes.objects.get(trn=trn)
			# obj.sn=request.POST['sn']
			# obj.s_types=request.POST['type']
			# obj.s_company=request.POST['company']
			# # obj.s_trd=request.POST['trd']
			# obj.s_trn=request.POST['trn']
			obj.s_dispute=request.POST['s_dispute']
			obj.s_remark=request.POST['s_remark']
			print('done')
			obj.save()
			
		except Exception as e:
			print(e)
	else:
		print('yes purchase')
		
		try:

			trn=TradeApproval.objects.get(p_trn=request.POST['trn'])
			
			obj=Disputes.objects.get(trn=trn)
			obj.p_dispute=request.POST['p_dispute']
			obj.p_remark=request.POST['p_remark']
			
			print('done')
			obj.save()
			
		except Exception as e:
			print(e)

	return HttpResponse()


@csrf_exempt
def EditInventory(request):

	type=request.POST['id']
	if type=='sales':
		print('yes sales')
		try:
			obj=SaveInventory.objects.get(trn=request.POST['trn'])
			# obj=Disputes.objects.get(trn=trn)
			obj.supplier=request.POST['supplier']
			obj.qtyin=request.POST['qtyin']
			obj.qtyout=request.POST['qtyout']
			obj.incoterm=request.POST['incoterm']
			obj.oldbalqtyvalue=request.POST['oldbalqtyvalue']
			obj.balanceqty=request.POST['balanceqty']
			obj.unit=request.POST['unit']
			obj.godownlocation=request.POST['godownlocation']
			obj.oldinventoryvalue=request.POST['oldinventoryvalue']
			obj.inventoryvalue=request.POST['inventoryvalue']
		
			print('done')
			obj.save()
			
		except Exception as e:
			print(e)

	Logging(request,'Inventory edited for '+ obj.trn)
	return HttpResponse()


def EditStock(request):
	print("editing "+request.POST['production_product-input'])
	countraw=request.POST['edit_count-raw']
	countadditive=request.POST['edit_count-additive']
	countpacking=request.POST['edit_countpacking']
	countblending=request.POST['edit_count-blending']
	print(countraw)
	print(countadditive)
	print(countpacking)
	print(countblending)

	try:
		obj=StockJournal.objects.get(product=request.POST['production_product-input'])
		obj.stockno=request.POST['stockjournal_num-input']
		obj.stockdate=request.POST['stockjournal_date-input']
		obj.qty=request.POST['production_quantity-input']
		obj.unit=request.POST['production_unit-input']
		obj.value=request.POST['production_value-input']
		obj.rate=request.POST['production_rateperunit']
		obj.production_remarks=request.POST['production_remarks-input']
		obj.consumption_remarks=request.POST['consumptionblockremarks']
		obj.save()

		obj.stockraw_set.all().delete()
		# printobj.stockraw_set.all())
		obj.stockadditive_set.all().delete()
		obj.stockpacking_set.all().delete()
		obj.stockconsumption_set.all().delete()

		for i in range(1,int(countraw)+1):
			print(i)
			try:
				
				raw=StockRaw.objects.create(product=obj,
				name=request.POST['consumptionproductraw-input'+str(i)],
				qtykg=request.POST['consumptionquantityraw-input'+str(i)],
				density=request.POST['consumptionquantitydensityraw-input'+str(i)],
				qtyliter=request.POST['consumptionquantityliterraw-input'+str(i)],
				ratekg=request.POST['consumptionquantityratekgraw-input'+str(i)],
				valuekg=request.POST['consumptionquantityvaluekgraw-input'+str(i)],
				rateliter=request.POST['consumptionquantityrateliter-input'+str(i)],
				valueliter=request.POST['consumptionquantityvalueliterraw-input'+str(i)])
				raw.save()
			except Exception as e:
				print(e)

		for i in range(1,int(countadditive)+1):
			print(i)
			try:
				additive=StockAdditive.objects.create(product=obj,
				name=request.POST['consumptionproductadditive-input'+str(i)],
				qtykg=request.POST['consumptionquantityadditive-input'+str(i)],
				density=request.POST['consumptionquantitydensityadditive-input'+str(i)],
				qtyliter=request.POST['consumptionquantityliteradditive-input'+str(i)],
				ratekg=request.POST['consumptionquantityratekgadditive-input'+str(i)],
				valuekg=request.POST['consumptionquantityvaluekgadditive-input'+str(i)],
				rateliter=request.POST['consumptionquantityrateliteradditive-input'+str(i)],
				valueliter=request.POST['consumptionquantityvalueliteradditive-input'+str(i)])
				additive.save()
			except Exception as e:
				print(e)

		for i in range(1,int(countpacking)+1):
			print(i)
			try:
				pack=StockPacking.objects.create(product=obj,
				name=request.POST['consumptionproductpacking-input'+str(i)],
				qty=request.POST['consumptionquantitypacking-input'+str(i)],
				unit=request.POST['consumptionunitpacking-input'+str(i)],
				rate=request.POST['consumptionquantityratepacking-input'+str(i)],
				value=request.POST['consumptionquantityvaluepacking-input'+str(i)])
				pack.save()
			except Exception as e:
				print(e)


		for i in range(1,int(countblending)+1):
			print(i)
			try:
				consumption=StockConsumption.objects.create(product=obj,
				name=request.POST['consumptionproductblending-input'+str(i)],
				qty=request.POST['consumptionquantityblending-input'+str(i)],
				unit=request.POST['consumptionunitblending-input'+str(i)],
				rate=request.POST['consumptionquantityrateblending-input'+str(i)],
				value=request.POST['consumptionquantityvalueblending-input'+str(i)])
				consumption.save()
			except Exception as e:
				print(e)

		# sn=SnStock.objects.create(sn=request.POST['stockjournal_num-input'])
		# sn.save()
		print('saved')
		


		Logging(request,'Stock Journal edited for '+request.POST['production_product-input'])
		
	except Exception as e:
		print(e)
	
	
	return redirect('home:stocks')

@csrf_exempt
def AmendValues(request):
	trn=request.POST['trn']
	print(trn)
	try:
		if TradeApproval.objects.filter(trn=trn).exists():
			trade=TradeApproval.objects.get(trn=trn)
			print(trade)
			data={'sn':trade.sn,'company':trade.company,'trd':trade.trd,'trn':trade.trn,'types':trade.types,
			'product':trade.product,'origin':trade.origin,'client':trade.client,'address':trade.address,
			'tcq':trade.tcq,'contractUnit':trade.contractUnit,'tolerance':trade.tolerance,'packing':trade.packing,
			'tuq':trade.tuq,'tuqUnit':trade.tuqUnit,'contractBalanceQty':trade.contractBalanceQty,
			'contractBalanceUnit':trade.contractBalanceUnit,'ratePMT':trade.ratePMT,'commissionAgent':trade.commissionAgent,
			'commissionRate':trade.commissionRate,'logisticProvider':trade.logisticProvider,'estimatedLogisticsCost':trade.estimatedLogisticsCost,
			'paymentTerm':trade.paymentTerm,'incoterm':trade.incoterm,'pol':trade.pol,'pod':trade.pod,
			'etd':trade.etd,'eta':trade.eta,'remarks':trade.remarks,'manager1':trade.manager1,'manager2':trade.manager2,
			'approve1':trade.approve1,'approve2':trade.approve2}
		else:
			data={}
	except Exception as e:
		print(e)
		
	return JsonResponse(data)

@csrf_exempt
def GetTradeApproval(request):
	types=request.POST['type']
	print(types)
	try:
		if types=="salestrade":
			if TradeApproval.objects.filter(Q(types='Sales',trade_status='')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Sales',trade_status='')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="purchasetrade":
			if TradeApproval.objects.filter(Q(types='Purchase',trade_status='')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Purchase',trade_status='')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="salesamendment":
			if TradeApproval.objects.filter(Q(types='Sales Amendment',trade_status='')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Sales Amendment',trade_status='')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="purchaseamendment":
			if TradeApproval.objects.filter(Q(types='Purchase Amendment',trade_status='')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Purchase Amendment',trade_status='')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="cancelsales":
			if TradeApproval.objects.filter(Q(types='Cancel Sales',trade_status='')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Cancel Sales',trade_status='')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="cancelpurchase":
			if TradeApproval.objects.filter(Q(types='Cancel Purchase',trade_status='')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Cancel Purchase',trade_status='')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
	except Exception as e:
		
		ctx={'data':None}
	
	return JsonResponse(data)

@csrf_exempt
def GetTradeApproved(request):
	types=request.POST['type']
	print(types)
	try:
		if types=="salestrade":
			if TradeApproval.objects.filter(Q(types='Sales',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Sales',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				# print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="purchasetrade":
			if TradeApproval.objects.filter(Q(types='Purchase',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Purchase',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				# print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="salesamendment":
			if TradeApproval.objects.filter(Q(types='Sales Amendment',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Sales Amendment',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="purchaseamendment":
			if TradeApproval.objects.filter(Q(types='Purchase Amendment',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Purchase Amendment',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="cancelsales":
			if TradeApproval.objects.filter(Q(types='Cancel Sales',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Cancel Sales',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="cancelpurchase":
			if TradeApproval.objects.filter(Q(types='Cancel Purchase',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Cancel Purchase',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="pending":
			pending=[]
			if SalesAndPurchase.objects.all().exists():
				t=TradeApproval.objects.all()
				for i in t:
				# print(i.trn)
					if SalesAndPurchase.objects.filter(trn__trn=i.trn).exists():
						pass
					else:
						p=model_to_dict(i)
						pending.append(p)
						# print()
				ctx={'data':pending}
				return JsonResponse(ctx)
				
	except Exception as e:
		
		ctx={'data':None}
	
	return JsonResponse(data)

@csrf_exempt
def GetPresale(request):
	types=request.POST['type']
	print(types)
	try:
		if types == "salestrade":
			if TradeApproval.objects.filter(Q(types='Sales',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Sales',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)
				
				ctx={'data':data}
				return JsonResponse(ctx)

		if types=="purchasetrade":
			if TradeApproval.objects.filter(Q(types='Purchase',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Purchase',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				# print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="salesamendment":
			if TradeApproval.objects.filter(Q(types='Sales Amendment',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Sales Amendment',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="purchaseamendment":
			if TradeApproval.objects.filter(Q(types='Purchase Amendment',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Purchase Amendment',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="cancelsales":
			if TradeApproval.objects.filter(Q(types='Cancel Sales',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Cancel Sales',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
		if types=="cancelpurchase":
			if TradeApproval.objects.filter(Q(types='Cancel Purchase',trade_status='Approved')).exists():
				
				data=[]
				records=TradeApproval.objects.filter(Q(types='Cancel Purchase',trade_status='Approved')).order_by('-trn')
				for i in records:
					i=model_to_dict(i)
					data.append(i)

				print(data)
				ctx={'data':data}
				return JsonResponse(ctx)
	except Exception as e:
		
		ctx={'data':None}
	
		return JsonResponse(ctx)

@csrf_exempt
def GetPrepayment(request):
	types=request.POST['type']
	print(types)
	try:
		if types=="salestrade":
			data=[]
			trn=[]
			records=PrePayments.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Sales":
					if TradeApproval.objects.filter(trn=i.trn.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			# print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="purchasetrade":
			data=[]
			trn=[]
			records=PrePayments.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Purchase":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			# print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="salesamendment":
			data=[]
			trn=[]
			records=PrePayments.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Sales Amendment":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			# print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="purchaseamendment":
			data=[]
			trn=[]
			records=PrePayments.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Purchase Amendment":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			# print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="cancelsales":
			data=[]
			trn=[]
			records=PrePayments.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Cancel Sales":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			# print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)
		if types=="cancelpurchase":
			data=[]
			trn=[]
			records=PrePayments.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Cancel Purchase":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			# print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)
	except Exception as e:
		
		ctx={'data':None}
	
	return JsonResponse(data)

@csrf_exempt
def GetSalesPurchase(request):
	types=request.POST['type']
	print(types)
	try:
		if types=="salestrade":
			data=[]
			trn=[]
			records=SalesAndPurchase.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Sales":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="purchasetrade":
			data=[]
			trn=[]
			records=SalesAndPurchase.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Purchase":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="salesamendment":
			data=[]
			trn=[]
			records=SalesAndPurchase.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Sales Amendment":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="purchaseamendment":
			data=[]
			trn=[]
			records=SalesAndPurchase.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Purchase Amendment":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="cancelsales":
			data=[]
			trn=[]
			records=SalesAndPurchase.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Cancel Sales":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)
		if types=="cancelpurchase":
			data=[]
			trn=[]
			records=SalesAndPurchase.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Cancel Purchase":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)
	except Exception as e:
		
		ctx={'data':None}
	
	return JsonResponse(data)

@csrf_exempt
def GetExtras(request):
	types=request.POST['type']
	print(types)
	try:
		if types=="salestrade":
			data=[]
			trn=[]
			records=ExtraCost.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Sales":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="purchasetrade":
			data=[]
			trn=[]
			records=ExtraCost.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Purchase":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="salesamendment":
			data=[]
			trn=[]
			records=ExtraCost.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Sales Amendment":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="purchaseamendment":
			data=[]
			trn=[]
			records=ExtraCost.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Purchase Amendment":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="cancelsales":
			data=[]
			trn=[]
			records=ExtraCost.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Cancel Sales":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)
		if types=="cancelpurchase":
			data=[]
			trn=[]
			records=ExtraCost.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Cancel Purchase":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)
	except Exception as e:
		
		ctx={'data':None}
	
	return JsonResponse(data)

@csrf_exempt
def GetFinance(request):
	types=request.POST['type']
	print(types)
	try:
		if types=="salestrade":
			data=[]
			trn=[]
			records=PaymentAndFinance.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Sales":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="purchasetrade":
			data=[]
			trn=[]
			records=PaymentAndFinance.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Purchase":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="salesamendment":
			data=[]
			trn=[]
			records=PaymentAndFinance.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Sales Amendment":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="purchaseamendment":
			data=[]
			trn=[]
			records=PaymentAndFinance.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Purchase Amendment":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)

		if types=="cancelsales":
			data=[]
			trn=[]
			records=PaymentAndFinance.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Cancel Sales":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)
		if types=="cancelpurchase":
			data=[]
			trn=[]
			records=PaymentAndFinance.objects.all().order_by('-trn')
			for i in records:
				if i.trn.types=="Cancel Purchase":
					if TradeApproval.objects.filter(trn=i.trn).exists():
						trade=TradeApproval.objects.get(trn=i.trn)
						trade=model_to_dict(trade)
						trn.append(trade)
					
					
					i=model_to_dict(i)
					data.append(i)

			print(data)
			ctx={'data':data,'trn':trn}
			return JsonResponse(ctx)
	except Exception as e:
		
		ctx={'data':None}
	
	return JsonResponse(data)


def GetQtyApprovedDetailPurchase(request):
	if SalesAndPurchase.objects.filter(trn__types__contains="Purchase").exists():
		trade=SalesAndPurchase.objects.filter(trn__types__contains="Purchase")
	else:
		trade=None

	return render(request,"quantityapprovedtablepurchase.html",{'trade':trade})

@csrf_exempt
def GetQtyApprovedDetailPurchaseHelper(request):
	if SalesAndPurchase.objects.filter(trn__types__contains="Purchase").exists():
		trade=SalesAndPurchase.objects.filter(trn__types__contains="Purchase")
	else:
		trade=None

	return render(request,"quantityapprovedtablepurchase.html",{'trade':trade})

def GetQtyApprovedDetailSales(request):
	if SalesAndPurchase.objects.filter(trn__types__contains="Sales").exists():
		trade=SalesAndPurchase.objects.filter(trn__types__contains="Sales")
	else:
		trade=None
	return render(request,"quantityapprovedtablesales.html",{'trade':trade})

@csrf_exempt
def GetQtyApprovedDetailSalesHelper(request):
	types=request.POST['types']
	records=[]
	trns=[]

	if SalesAndPurchase.objects.filter(trn__types__contains="Sales").exists():
		trade=SalesAndPurchase.objects.filter(trn__types__contains="Sales")
		for i in trade:
			record=model_to_dict(i)
			records.append(record)
			t=TradeApproval.objects.get(trn=i.trn.trn)
			trn=model_to_dict(t)
			trns.append(trn)
	
	return JsonResponse({'data':records,'trn':trns})


@csrf_exempt
def FilterPL(request):
	year=request.POST['year']
	month=request.POST['month']
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	print(days)
	# print(type(month))
	pls=[]
	trns=[]
	sps=[]
	trns_p=[]
	if PL.objects.all().exists():
		pl=PL.objects.all()
		filterDay=None
		for i in pl:
			trn=TradeApproval.objects.get(trn=i.trn.trn)
			if SalesAndPurchase.objects.filter(trn=trn).exists():
				sp=SalesAndPurchase.objects.get(trn=trn)
					# s=model_to_dict(sp.invoiceDate)
				# sps.append(sp.invoiceDate)
				filterDay=sp.invoiceDate

				# print("filter day",str(filterDay))
			else:
				sps.append('None')
				# print(sps)
			trn_p=TradeApproval.objects.get(trn=i.p_trn)
			if sp.invoiceDate != "NA":
				date1=datetime.strptime(sp.invoiceDate ,'%d/%m/%Y')
				# print(sp.invoiceDate)
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
			# print(date1)
				if date1<d2 and date1>d1:
				# print(sp.invoiceDate)
				# print(d1,date1,d2)
					i=model_to_dict(i)
					trn1=model_to_dict(trn)
					pls.append(i)
					trns.append(trn1)
					trns_p.append(trn_p.client)
					sps.append(sp.invoiceDate)

				
	# print(sps)
	data={'data':pls,'trns':trns,'sps':sps,'trns_p':trns_p}	
	# print(data)
	return JsonResponse(data)

@csrf_exempt
def FilterS(request):
	year=request.POST['year']
	month=request.POST['month']
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	print(type(year))
	print(type(month))
	sps=[]
	trns=[]
	if SalesAndPurchase.objects.all().exists():
		sp=SalesAndPurchase.objects.all()
		for i in sp:
			if i.trn.types=='Sales':
				trn=TradeApproval.objects.get(trn=i.trn.trn)
				date1=datetime.strptime(i.trn.trd,'%d/%m/%Y')
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
				if date1<=d2 and date1>=d1:
					i=model_to_dict(i)
					trn=model_to_dict(trn)
					sps.append(i)
					trns.append(trn)
	data={'data':sps,'trns':trns}	
	print(data)
	return JsonResponse(data)

@csrf_exempt
def FilterP(request):
	year=request.POST['year']
	month=request.POST['month']
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	print(type(year))
	print(type(month))
	sps=[]
	trns=[]
	if SalesAndPurchase.objects.all().exists():
		sp=SalesAndPurchase.objects.all()
		for i in sp:
			if i.trn.types=='Purchase':
				trn=TradeApproval.objects.get(trn=i.trn.trn)
				date1=datetime.strptime(i.trn.trd,'%d/%m/%Y')
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
				if date1<=d2 and date1>=d1:
					i=model_to_dict(i)
					trn=model_to_dict(trn)
					sps.append(i)
					trns.append(trn)
	data={'data':sps,'trns':trns}	
	print(data)
	return JsonResponse(data)


from calendar import monthrange
@csrf_exempt
def FinanceDate(request):
	year=int(request.POST['year'])
	month=int(request.POST['month'])
	a=monthrange(year,month)
	print(a[0])
	print(a[1])
	first=datetime(year=year, month=month, day=1).date()
	last=datetime(year=year, month=month, day=a[1]).date()
	# print(first)

	payments=[]
	trn=[]
	records=PaymentAndFinance.objects.all()
	for i in records:
		if i.paymentDate != 'NA':
			paymentdate=datetime.strptime(i.paymentDate,'%d/%m/%Y').date()
			if paymentdate >= first:
				if paymentdate <= last:
					paymentdate=model_to_dict(i)
					payments.append(paymentdate)
					t=TradeApproval.objects.get(trn=i.trn.trn)
					t=model_to_dict(t)
					trn.append(t)
	
	return JsonResponse({'data':payments,'trn':trn})



@csrf_exempt
def SPDate(request):
	types=request.POST['types']
	year=int(request.POST['year'])
	month=int(request.POST['month'])
	a=monthrange(year,month)
	# print(a[0])
	# print(a[1])
	first=datetime(year=year, month=month, day=1).date()
	last=datetime(year=year, month=month, day=a[1]).date()
	# print(first)

	sales=[]
	purchase=[]
	trn=[]

	records=SalesAndPurchase.objects.all()
	if types == 'Sales':
		for i in records:
			if i.invoiceDate != 'NA' and i.trn.types == 'Sales':
				invoicedate=datetime.strptime(i.invoiceDate,'%d/%m/%Y').date()
				if invoicedate >= first:
					if invoicedate <= last:
						invoicedate=model_to_dict(i)
						sales.append(invoicedate)
						t=TradeApproval.objects.get(trn=i.trn.trn)
						t=model_to_dict(t)
						trn.append(t)
		return JsonResponse({'data':sales,'trn':trn})

	if types == 'Purchase':
		for i in records:
			if i.invoiceDate != 'NA' and i.trn.types == 'Purchase':
				invoicedate=datetime.strptime(i.invoiceDate,'%d/%m/%Y').date()
				if invoicedate >= first:
					if invoicedate <= last:
						invoicedate=model_to_dict(i)
						purchase.append(invoicedate)
						t=TradeApproval.objects.get(trn=i.trn.trn)
						t=model_to_dict(t)
						trn.append(t)
	
		return JsonResponse({'data':purchase,'trn':trn})

@csrf_exempt
def ApprovedFilter(request):
	year=request.POST['year']
	month=request.POST['month']
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	print(year)
	print(month)
	# sps=[]
	trns=[]
	if TradeApproval.objects.all().exists():
		t=TradeApproval.objects.all()
		# print(t)
		for i in t:
			if i.trade_status == 'Approved':
				# trn=TradeApproval.objects.get(trn=i.trn)
				date1=datetime.strptime(i.trd,'%d/%m/%Y')
				# print(date1)
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
				if date1<=d2 and date1>=d1:
					i=model_to_dict(i)
					# trn=model_to_dict(trn)
					# sps.append(i)
					trns.append(i)
	data={'data':trns}	
	# print(data)
	return JsonResponse(data)

@csrf_exempt
def ApproveSP(request):
	trn=request.POST['trn']
	print(trn+' doing')
	if SalesAndPurchase.objects.filter(trn__trn__contains=trn).exists():
		sp=SalesAndPurchase.objects.get(trn__trn__contains=trn)
		sp.reviewed=True
		sp.save()
	Logging(request,'SalesAndPurchase approved for '+ str(trn))
	return redirect('home:salesPurchase')


import xlwt 
@csrf_exempt
def ExportApproved(request,approved):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="TradeApproved.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('TradeApproved')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Company', 'TRD', 'TRN','Type','Product Code','Product Name','Country of Origin','Party','Address','Trade Approved Date','Trade Status',
	'Trade Contract Qty','Trade Qty','Trade Unit','Contract Balance Qty','Rate PMT','Commission Agent','Commission Rate',
	'Logistic Provider', 'Est. Logistic Cost','Payment Term','Incoterm','POL','POD','ETD','ETA','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	if approved == 'all':
		print('in all excel')
		trns = TradeApproval.objects.all()

		for row in trns:
			if row.trade_status == 'Approved':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approved == 'salestrade':
		print('in sales excel')
		trns = TradeApproval.objects.filter(types='Sales')

		for row in trns:
			if row.trade_status == 'Approved':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approved == 'purchasetrade':
		trns = TradeApproval.objects.filter(types='Purchase')

		for row in trns:
			if row.trade_status == 'Approved':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approved == 'cancelsales':
		trns = TradeApproval.objects.filter(types='Cancel Sales')

		for row in trns:
			if row.trade_status == 'Approved':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)
					
	if approved == 'cancelpurchase':
		trns = TradeApproval.objects.filter(types='Cancel Purchase')

		for row in trns:
			if row.trade_status == 'Approved':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approved == 'salesamendment':
		trns = TradeApproval.objects.filter(types='Sales Amendment')

		for row in trns:
			if row.trade_status == 'Approved':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approved == 'purchaseamendment':
		trns = TradeApproval.objects.filter(types='Purchase Amendment')

		for row in trns:
			if row.trade_status == 'Approved':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)
	if approved == 'pending':
		trns=[]
		if SalesAndPurchase.objects.all().exists():
				t=TradeApproval.objects.all()
				for i in t:
				# print(i.trn)
					if SalesAndPurchase.objects.filter(trn__trn=i.trn).exists():
						pass
					else:
						trns.append(i)
		for row in trns:
			if row.trade_status == 'Approved':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	wb.save(response)
	return response

@csrf_exempt
def ExportApprovedFilter(request,year,month):
	# .
	year=year
	month=month
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	print(year)
	print(month)
	sps=[]
	trns=[]
	if TradeApproval.objects.all().exists():
		t=TradeApproval.objects.all()
	# 	print(t)
		for i in t:
			if i.trade_status == 'Approved':
				trn=TradeApproval.objects.get(trn=i.trn)
				date1=datetime.strptime(i.trd,'%d/%m/%Y')
				print(date1)
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
				if date1<=d2 and date1>=d1:
	# 				i=model_to_dict(i)
	# 				# trn=model_to_dict(trn)
	# 				# sps.append(i)
					trns.append(i)
	# data={'data':trns}	
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="TradeApproved.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Documents')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Company', 'TRD', 'TRN','Type','Product Code','Product Name','Country of Origin','Party','Address','Trade Approved Date','Trade Status',
	'Trade Contract Qty','Trade Qty','Trade Unit','Contract Balance Qty','Rate PMT','Commission Agent','Commission Rate',
	'Logistic Provider', 'Est. Logistic Cost','Payment Term','Incoterm','POL','POD','ETD','ETA','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	# trns = TradeApproval.objects.all()
	print('In filter date')
	for row in trns:
		if row.trade_status == 'Approved':
			record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportApproval(request,approval):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="TradeApprovals.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('TradeApproval')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Company', 'TRD', 'TRN','Type','Product Code','Product Name','Country of Origin','Party','Address','Trade Approved Date','Trade Status',
	'Trade Contract Qty','Trade Qty','Trade Unit','Contract Balance Qty','Rate PMT','Commission Agent','Commission Rate',
	'Logistic Provider', 'Est. Logistic Cost','Payment Term','Incoterm','POL','POD','ETD','ETA','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	if approval == 'all':
		trns = TradeApproval.objects.all()

		for row in trns:
			if row.trade_status == '':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'salestrade':
		trns = TradeApproval.objects.filter(types='Sales')

		for row in trns:
			if row.trade_status == '':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'purchasetrade':
		trns = TradeApproval.objects.filter(types='Purchase')

		for row in trns:
			if row.trade_status == '':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'cancelsales':
		trns = TradeApproval.objects.filter(types='Cancel Sales')

		for row in trns:
			if row.trade_status == '':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)
					
	if approval == 'cancelpurchase':
		trns = TradeApproval.objects.filter(types='Cancel Purchase')

		for row in trns:
			if row.trade_status == '':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'salesamendment':
		trns = TradeApproval.objects.filter(types='Sales Amendment')

		for row in trns:
			if row.trade_status == '':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'purchaseamendment':
		trns = TradeApproval.objects.filter(types='Purchase Amendment')

		for row in trns:
			if row.trade_status == '':
				record=[row.sn, row.company, row.trd, row.trn,row.types,row.product,row.baseproduct,row.origin,row.client,row.address,row.tad,row.trade_status,
				row.tcq,row.tuq,row.contractUnit,row.contractBalanceQty,row.ratePMT,row.commissionAgent,row.commissionRate,
				row.logisticProvider, row.estimatedLogisticsCost,row.paymentTerm,row.incoterm,row.pol,row.pod,row.etd,row.eta,row.remarks]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)

	wb.save(response)
	return response

@csrf_exempt
def ExportDoc(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="users.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Documents')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Type', 'Company', 'TRD','TRN','Party','Purchase Order No.','Purchase Order Date','Sales Order No.','Sales Order Date']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = TradeApproval.objects.all()

	for row in trns:
		if row.trade_status != '':
			record=[row.sn, row.types, row.company, row.trd,row.trn,row.client,row.po_number,row.po_date,row.so_number,row.so_date]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response


@csrf_exempt
def ExportPre(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="prepayments.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Prepayments')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Type', 'Company', 'TRD','TRN','Party','Due Date',
	'As per PI Cash/TT/Advance','LC Number/ Value','LC Issuing/Advising Bank/ Value','Advance Received From Buyers',
	'Advance Paid to Sellers','Received Date','Paid date','LC Expiry Date','Latest Date For Shipment','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = PrePayments.objects.all().order_by('trn')

	for row in trns:
		
		record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.dueDate,
		row.advance,row.lcNumberValue,row.lcIssuingBank,row.advanceFromBuyers,row.advanceToSellers,row.receivedDate,
		row.paidDate,row.lcExpiryDate,row.nextShipmentDate,row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportSP(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="users.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('SalesAndPurchase')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Type', 'Company', 'TRD','TRN','Party','Product Name','Trade Qty','Trade Unit','Rate PMT',
	'Invoice Date','Invoice Number','Invoice Amount','Commission Agent','Commission Amount','Packing List Details','Bill Number',
	'Bill Qty','Bill Date','Logistic Agent','Logistic Cost','Liner','ETA','ETD','Shipment Status','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = SalesAndPurchase.objects.all()

	for row in trns:
		
		record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,
		row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
		row.invoiceDate,row.invoiceNumber,row.invoiceAmount,row.commissionAgent,row.commissionAmount,row.packingListDetails,
		row.billNumber,row.billQty,row.billDate,row.logisticAgent,row.logisticCost,row.liner,row.eta,row.etd,row.shipmentStatus,
		row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response


@csrf_exempt
def ExportExtras(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="users.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('ExtraCost')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Type', 'Company', 'TRD','TRN','Party','Product Name','Trade Qty','Trade Unit','Rate PMT',
	'Bank Charges','Bill Fee','Bill Collection Charges','Other Charges','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = ExtraCost.objects.all()

	for row in trns:
		
		record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,
		row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
		row.bankCharges,row.billFee,row.billCollectionCharges,row.otherCharges,row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response


@csrf_exempt
def ExportFinance(request,approval):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="users.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('PurchaseAndFinance')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Type', 'Company', 'TRD','TRN','Party','Product Name','Trade Qty','Trade Unit','Rate PMT',
	'Balance Payment','Due Date','Payment','Payment Date','Balance Due','Payment Mode','Payment Status','Logistics Payment Due',
	'Logistics Provider','Commission Agent','Logistics Commission Due Date','Agent Commission Due Date','Agent Commission Paid',
	'Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	if approval == 'all':
		trns = PaymentAndFinance.objects.all()
		for row in trns:
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
			row.balancePayment,row.dueDate,row.payment,row.paymentDate,row.balanceDue,row.paymentMode,row.paymentStatus,
			row.logisticsPaymentDue,row.logisticsProvider,row.commissionAgent,row.logisticsCommissionDueDate,row.agentCommissionDueDate,
			row.agentCommissionPaid,row.remarks]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'salestrade':
		trns = PaymentAndFinance.objects.filter(trn__types__contains='Sales')
		for row in trns:
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
			row.balancePayment,row.dueDate,row.payment,row.paymentDate,row.balanceDue,row.paymentMode,row.paymentStatus,
			row.logisticsPaymentDue,row.logisticsProvider,row.commissionAgent,row.logisticsCommissionDueDate,row.agentCommissionDueDate,
			row.agentCommissionPaid,row.remarks]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)	

	if approval == 'purchasetrade':
		trns = PaymentAndFinance.objects.filter(trn__types__contains='Purchase')
		for row in trns:
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
			row.balancePayment,row.dueDate,row.payment,row.paymentDate,row.balanceDue,row.paymentMode,row.paymentStatus,
			row.logisticsPaymentDue,row.logisticsProvider,row.commissionAgent,row.logisticsCommissionDueDate,row.agentCommissionDueDate,
			row.agentCommissionPaid,row.remarks]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'cancelsales':
		trns = PaymentAndFinance.objects.filter(trn__types__contains='Sales Cancel')
		for row in trns:
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
			row.balancePayment,row.dueDate,row.payment,row.paymentDate,row.balanceDue,row.paymentMode,row.paymentStatus,
			row.logisticsPaymentDue,row.logisticsProvider,row.commissionAgent,row.logisticsCommissionDueDate,row.agentCommissionDueDate,
			row.agentCommissionPaid,row.remarks]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'cancelpurchase':
		trns = PaymentAndFinance.objects.filter(trn__types__contains='Purchase Cancel')
		for row in trns:
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
			row.balancePayment,row.dueDate,row.payment,row.paymentDate,row.balanceDue,row.paymentMode,row.paymentStatus,
			row.logisticsPaymentDue,row.logisticsProvider,row.commissionAgent,row.logisticsCommissionDueDate,row.agentCommissionDueDate,
			row.agentCommissionPaid,row.remarks]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'salesamendment':
		trns = PaymentAndFinance.objects.filter(trn__types__contains='Sales Amendment')
		for row in trns:
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
			row.balancePayment,row.dueDate,row.payment,row.paymentDate,row.balanceDue,row.paymentMode,row.paymentStatus,
			row.logisticsPaymentDue,row.logisticsProvider,row.commissionAgent,row.logisticsCommissionDueDate,row.agentCommissionDueDate,
			row.agentCommissionPaid,row.remarks]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)

	if approval == 'purchaseamendment':
		trns = PaymentAndFinance.objects.filter(trn__types__contains='Purchase Amendment')
		for row in trns:
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
			row.balancePayment,row.dueDate,row.payment,row.paymentDate,row.balanceDue,row.paymentMode,row.paymentStatus,
			row.logisticsPaymentDue,row.logisticsProvider,row.commissionAgent,row.logisticsCommissionDueDate,row.agentCommissionDueDate,
			row.agentCommissionPaid,row.remarks]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)

	wb.save(response)
	return response


@csrf_exempt
def ExportProfit(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="PL.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('ProfitAndLoss')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Type', 'Company', 'TRD','TRN','Sales Invoice Date','Party','Product Name','Trade Qty','Trade Unit','Rate PMT',
	'Purchase TRN','Sales Total Cost','Purchase Total Cost','Total Revenue From Sales','Gross Profit','Profit Per Drum','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = PL.objects.all()
	sps=[]
	for i in trns:
		if SalesAndPurchase.objects.filter(trn=i.trn).exists():
			sp=SalesAndPurchase.objects.get(trn=i.trn)
			sps.append(sp)
		else:
			sps.append("None")

	for row,s in zip(trns,sps):
		if s == "None":
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,"None",row.trn.client,row.trn.baseproduct,"None",row.trn.contractUnit,row.trn.ratePMT,
			row.p_trn,row.s_purchaseTotalCost,row.p_purchaseTotalCost,row.totalRevenueFromSales,row.grossProfit,row.profitPerDrum,
			row.remarks]
		else:
			
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,s.invoiceDate,row.trn.client,row.trn.baseproduct,s.billQty,row.trn.contractUnit,row.trn.ratePMT,
			row.p_trn,row.s_purchaseTotalCost,row.p_purchaseTotalCost,row.totalRevenueFromSales,row.grossProfit,row.profitPerDrum,
			row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response


@csrf_exempt
def ExportFilterProfit(request,year,month):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="PL.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('ProfitAndLoss')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Type', 'Company', 'TRD','TRN','Sales Invoice Date','Party','Product Name','Trade Qty','Trade Unit','Rate PMT',
	'Purchase TRN','Sales Total Cost','Purchase Total Cost','Total Revenue From Sales','Gross Profit','Profit Per Drum','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()

	year=year
	month=month
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	# print(type(year))
	# print(type(month))
	pls=[]
	trns=[]
	sps=[]
	trns_p=[]
	if PL.objects.all().exists():
		pl=PL.objects.all()
		for i in pl:
			trn=TradeApproval.objects.get(trn=i.trn.trn)
			if SalesAndPurchase.objects.filter(trn=trn).exists():
				sp=SalesAndPurchase.objects.get(trn=trn)
					# s=model_to_dict(sp.invoiceDate)
					# sps.append(sp)
					# print(sps)
			else:
				sps.append('None')
			trn_p=TradeApproval.objects.get(trn=i.p_trn)
			if sp.invoiceDate != "NA":
				date1=datetime.strptime(sp.invoiceDate,'%d/%m/%Y')
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
				if date1<d2 and date1>d1:
				# i=model_to_dict(i)
				# trn1=model_to_dict(trn)
					pls.append(i)
				# trns.append(trn1)
					trns_p.append(trn_p.client)
					sps.append(sp)

				
					# print(sps)
	for row,s in zip(pls,sps):
		if s == "None":
			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,"None",row.trn.client,row.trn.baseproduct,"None",row.trn.contractUnit,row.trn.ratePMT,
			row.p_trn,row.s_purchaseTotalCost,row.p_purchaseTotalCost,row.totalRevenueFromSales,row.grossProfit,row.profitPerDrum,
			row.remarks]
		else:
			

			record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,s.invoiceDate,row.trn.client,row.trn.baseproduct,s.billQty,row.trn.contractUnit,row.trn.ratePMT,
			row.p_trn,row.s_purchaseTotalCost,row.p_purchaseTotalCost,row.totalRevenueFromSales,row.grossProfit,row.profitPerDrum,
			row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportKyc(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="users.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Kyc')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Date','Name','Company RegNo','Reg.Address','Mailing Address','Telephone','Fax','Person 1','Designation 1',
	'Mobile 1','Email 1','Person 2','Designation 2','Mobile 2','Email 2','Banker','Address','Swift Code','Account Number']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = Kyc.objects.all()

	for row in trns:
		
		record=[row.date,row.name,row.companyRegNo,row.regAddress,row.mailingAddress,row.telephone,row.fax,row.person1,
		row.designation1,row.mobile1,row.email1,row.person2,row.designation2,row.mobile2,row.email2,row.banker,row.address,
		row.swiftCode,row.accountNumber]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportSales(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Sales.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Sales')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['TRN','Product','Quantity','Rate','Value','Buyer/Seller Name','Invoice Number','Invoice Date']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = SalesAndPurchase.objects.filter(trn__types__contains="Sales")

	for row in trns:
		
		record=[row.trn.trn,row.trn.baseproduct,row.trn.tuq,row.trn.ratePMT,float(row.trn.tuq)*float(row.trn.ratePMT),row.trn.client,row.invoiceNumber,row.invoiceDate]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportPurchase(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Purchases.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Purchases')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['TRN','Product','Quantity','Rate','Value','Buyer/Seller Name','Invoice Number','Invoice Date']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = SalesAndPurchase.objects.filter(trn__types__contains="Purchase")

	for row in trns:
		
		record=[row.trn.trn,row.trn.baseproduct,row.trn.tuq,row.trn.ratePMT,float(row.trn.tuq)*float(row.trn.ratePMT),row.trn.client,row.invoiceNumber,row.invoiceDate]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportSalesFilter(request,year,month):
	# .
	year=year
	month=month
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	print(year)
	print(month)
	# sps=[]
	trns=[]
	if SalesAndPurchase.objects.all().exists():
		sp=SalesAndPurchase.objects.all()
		for i in sp:
			if i.trn.types=='Sales' and i.invoiceDate != 'NA':
				trn=TradeApproval.objects.get(trn=i.trn.trn)
				date1=datetime.strptime(i.invoiceDate,'%d/%m/%Y')
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
				if date1<=d2 and date1>=d1:
					# i=model_to_dict(i)
					# trn=model_to_dict(trn)
					print()
					trns.append(i)
	# print(trns)
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Sales.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Sales')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['TRN','Product','Quantity','Rate','Value','Buyer/Seller Name','Invoice Number','Invoice Date']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	# trns = TradeApproval.objects.all()
	print('In filter date')
	for row in trns:
		
		record=[row.trn.trn,row.trn.baseproduct,row.trn.tuq,row.trn.ratePMT,float(row.trn.tuq)*float(row.trn.ratePMT),row.trn.client,row.invoiceNumber,row.invoiceDate]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportPurchaseFilter(request,year,month):
	year=year
	month=month
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	print(year)
	print(month)
	# sps=[]
	trns=[]
	if SalesAndPurchase.objects.all().exists():
		sp=SalesAndPurchase.objects.all()
		for i in sp:
			if i.trn.types=='Purchase' and i.invoiceDate != 'NA':
				trn=TradeApproval.objects.get(trn=i.trn.trn)
				date1=datetime.strptime(i.invoiceDate,'%d/%m/%Y')
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
				if date1<=d2 and date1>=d1:
					# i=model_to_dict(i)
					# trn=model_to_dict(trn)
					print()
					trns.append(i)
	# print(trns)
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Purchase.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Purchase')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['TRN','Product','Quantity','Rate','Value','Buyer/Seller Name','Invoice Number','Invoice Date']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	# trns = TradeApproval.objects.all()
	print('In filter date')
	for row in trns:
		
		record=[row.trn.trn,row.trn.baseproduct,row.trn.tuq,row.trn.ratePMT,float(row.trn.tuq)*float(row.trn.ratePMT),row.trn.client,row.invoiceNumber,row.invoiceDate]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportFinanceFilter(request,year,month):
	# .
	year=year
	month=month
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	print(year)
	print(month)
	# sps=[]
	trns=[]
	if PaymentAndFinance.objects.all().exists():
		sp=PaymentAndFinance.objects.all()
		for i in sp:
			if i.paymentDate != 'NA':
				trn=TradeApproval.objects.get(trn=i.trn.trn)
				date1=datetime.strptime(i.paymentDate,'%d/%m/%Y')
				d1=datetime(year,month,1)
				d2=datetime(year,month,days)
				if date1<=d2 and date1>=d1:
					
					print()
					trns.append(i)
	# print(trns)
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Sales.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Sales')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['SN', 'Type', 'Company', 'TRD','TRN','Party','Product Name','Trade Qty','Trade Unit','Rate PMT',
	'Balance Payment','Due Date','Payment','Payment Date','Balance Due','Payment Mode','Payment Status','Logistics Payment Due',
	'Logistics Provider','Commission Agent','Logistics Commission Due Date','Agent Commission Due Date','Agent Commission Paid',
	'Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	# trns = TradeApproval.objects.all()
	print('In filter date')
	for row in trns:
		
		record=[row.trn.sn, row.trn.types, row.trn.company, row.trn.trd,row.trn.trn,row.trn.client,row.trn.baseproduct,row.trn.tuq,row.trn.contractUnit,row.trn.ratePMT,
		row.balancePayment,row.dueDate,row.payment,row.paymentDate,row.balanceDue,row.paymentMode,row.paymentStatus,
		row.logisticsPaymentDue,row.logisticsProvider,row.commissionAgent,row.logisticsCommissionDueDate,row.agentCommissionDueDate,
		row.agentCommissionPaid,row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ApproveKyc1(request):
	name=request.POST['name']
	print(name)
	try:
		kyc=Kyc.objects.get(name=name)
		kyc.approve1=True
		kyc.save()
		print(kyc.approve1)
	except Exception as e:
		print(e)
	# Logging(request,'KYC approved for '+ str(kyc))
	return redirect('home:kyc')

@csrf_exempt
def ApproveKyc2(request):
	name=request.POST['name']
	try:
		kyc=Kyc.objects.get(name=name)
		kyc.approve2=True
		kyc.save()
	except Exception as e:
		print(e)
	# Logging(request,'KYC approved for '+ str(kyc))
	return redirect('home:kyc')

# @csrf_exempt
# def ExportDashPre(request):
# 	print('in here')
# 	response = HttpResponse(content_type='application/ms-excel')
# 	response['Content-Disposition'] = 'attachment; filename="paymentandfinancedue.xls"'

# 	wb = xlwt.Workbook(encoding='utf-8')
# 	ws = wb.add_sheet('Finance Due')

#     # Sheet header, first row
# 	row_num = 0

# 	font_style = xlwt.XFStyle()
# 	font_style.font.bold = True

# 	columns = ['TRN','Company Name','LC no/value','Due Date','Due Amount']

# 	for col_num in range(len(columns)):
# 		ws.write(row_num, col_num, columns[col_num], font_style)

# 	font_style = xlwt.XFStyle()
	
# 	trns = PrePayments.objects.all()
# 	print('printing here')
# 	for row in trns:
# 		if row.dueDate != 'NA':
# 			if row.trn.types == 'Sales':
# 				remaining=row.advance-row.advanceFromBuyers
# 			if row.trn.types == 'Purchase':
# 				remaining=row.advance-row.advanceToSellers

# 			due=datetime.strptime(row.dueDate,'%Y-%m-%d').date()
# 			# if due<date.today():
# 			if remaining>0:
# 				# pre.append(i)
			
# 			# print(row.balanceDue)
# 			# pre.append(i)
# 				record=[row.trn.trn,row.trn.client,row.lcNumberValue,row.dueDate,remaining]

# 				row_num += 1
# 				for col_num in range(len(record)):
# 					ws.write(row_num, col_num, record[col_num], font_style)
# 	wb.save(response)
# 	return response

@csrf_exempt
def CheckPre(request):
	print('in here')
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="dueprepayments.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Prepayments Due')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['TRN','Company Name','LC no/value','Due Date','Due Amount']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = PrePayments.objects.all()
	print('printing here')
	for row in trns:
		if row.dueDate != 'NA':
			if row.trn.types == 'Sales':
				remaining=row.advance-row.advanceFromBuyers
			if row.trn.types == 'Purchase':
				remaining=row.advance-row.advanceToSellers

			due=datetime.strptime(row.dueDate,'%Y-%m-%d').date()
			# if due<date.today():
			if remaining>0:
				# pre.append(i)
			
			# print(row.balanceDue)
			# pre.append(i)
				record=[row.trn.trn,row.trn.client,row.lcNumberValue,row.dueDate,remaining]

				row_num += 1
				for col_num in range(len(record)):
					ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response
	# return HttpResponse('hello')

# @csrf_exempt
# def ExportDashFinance(request):
# 	print('in here')
# 	response = HttpResponse(content_type='application/ms-excel')
# 	response['Content-Disposition'] = 'attachment; filename="paymentandfinancedue.xls"'

# 	wb = xlwt.Workbook(encoding='utf-8')
# 	ws = wb.add_sheet('Finance Due')

#     # Sheet header, first row
# 	row_num = 0

# 	font_style = xlwt.XFStyle()
# 	font_style.font.bold = True

# 	columns = ['TRN','Type','Company Name','Due Date','Due Amount']

# 	for col_num in range(len(columns)):
# 		ws.write(row_num, col_num, columns[col_num], font_style)

# 	font_style = xlwt.XFStyle()
	
# 	trns = PaymentAndFinance.objects.all()
# 	print('printing here')
# 	for row in trns:
# 		if row.balanceDue>0.0:
			
# 			# print(row.balanceDue)
# 			# pre.append(i)
# 			record=[row.trn.trn,row.trn.types,row.trn.client,row.dueDate,row.balanceDue]

# 			row_num += 1
# 			for col_num in range(len(record)):
# 				ws.write(row_num, col_num, record[col_num], font_style)
# 	wb.save(response)
# 	return response


@csrf_exempt
def CheckFinance(request):
	print('in here')
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="paymentandfinancedue.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Finance Due')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['TRN','Type','Company Name','Due Date','Due Amount']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	trns = PaymentAndFinance.objects.all()
	print('printing here')
	for row in trns:
		if row.balanceDue>0.0:
			
			# print(row.balanceDue)
			# pre.append(i)
			record=[row.trn.trn,row.trn.types,row.trn.client,row.dueDate,row.balanceDue]

			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response
	# return HttpResponse('Hi')
@csrf_exempt
def DelApproval(request):
	trn=request.POST['trn']
	# print(str(trn)+'in here')
	if TradeApproval.objects.filter(trn=trn).exists():
		t=TradeApproval.objects.get(trn=trn)
		t.delete()
		Logging(request,'Trade Approval deleted, '+ str(trn))
		return JsonResponse({'result':'Done'})
	return JsonResponse({'result':'Error'})

@csrf_exempt
def DelApproved(request):
	trn=request.POST['trn']
	# print(str(trn)+'in here')
	if TradeApproval.objects.filter(trn=trn).exists():
		t=TradeApproval.objects.get(trn=trn)
		t.delete()
		Logging(request,'Trade Approved deleted, '+ str(trn))
		return JsonResponse({'result':'Done'})
	return JsonResponse({'result':'Error'})

@csrf_exempt
def DelPrepayment(request):
	trn=request.POST['trn']
	# print(str(trn)+'in here')
	if PrePayments.objects.filter(trn__trn__exact=trn).exists():
		t=PrePayments.objects.get(trn__trn__exact=trn)
		t.delete()
		Logging(request,'Prepayment deleted, '+ str(trn))
		return JsonResponse({'result':'Done'})
	return JsonResponse({'result':'Error'})

@csrf_exempt
def DelSP(request):
	trn=request.POST['trn']
	# print(str(trn)+'in here')
	if SalesAndPurchase.objects.filter(trn__trn__exact=trn).exists():
		t=SalesAndPurchase.objects.get(trn__trn__exact=trn)
		t.delete()
		Logging(request,'SalesAndPurchase deleted, '+ str(trn))
		return JsonResponse({'result':'Done'})
	return JsonResponse({'result':'Error'})

@csrf_exempt
def DelExtra(request):
	trn=request.POST['trn']
	# print(str(trn)+'in here')
	if ExtraCost.objects.filter(trn__trn__exact=trn).exists():
		t=ExtraCost.objects.get(trn__trn__exact=trn)
		t.delete()
		Logging(request,'Extra Cost deleted, '+ str(trn))
		return JsonResponse({'result':'Done'})
	return JsonResponse({'result':'Error'})

@csrf_exempt
def DelFinance(request):
	trn=request.POST['trn']
	# print(str(trn)+'in here')
	if PaymentAndFinance.objects.filter(trn__trn__exact=trn).exists():
		t=PaymentAndFinance.objects.get(trn__trn__exact=trn)
		t.delete()
		Logging(request,'PaymentAndFinance deleted, '+ str(trn))
		return JsonResponse({'result':'Done'})
	return JsonResponse({'result':'Error'})
@csrf_exempt
def DelPnL(request):
	trn=request.POST['trn']
	# print(str(trn)+'in here')
	if PL.objects.filter(trn__trn__exact=trn).exists():
		t=PL.objects.get(trn__trn__exact=trn)
		t.delete()
		Logging(request,'ProfitAndLoss deleted, '+ str(trn))
		return JsonResponse({'result':'Done'})
	return JsonResponse({'result':'Error'})


@csrf_exempt
def ExportInventory(request):
	# product=productname
	# print(product)
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="inventory.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Inventory')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['TRN','Trade Type','Product','Date of Purchase/Sales','Invoice No','Buyer/Supplier Name',
	'Purchase/Sales Price','Incoterm','Quantity','Value','Bill No.','Bill Date','Logistic Agent','Liner','ETD','ETA','Inventory']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	sp=[]
	pro=[]
	products=TradeApproval.objects.order_by().values_list('baseproduct',flat=True).distinct().order_by('baseproduct')
	for i in products:#reading names with redundancy
		sp.append('break')#for new line
		sps=SalesAndPurchase.objects.filter(trn__baseproduct__exact=i)#all trns with name i
		if sps.count() != 0:#if not empty
			pro.append(i)#add for display
		for j in sps:#each element from i
			sp.append(j)
		
	# print(inventory)
	print('printing here')
	val=0
	for row in sp:

		if row != 'break' and row.trn.types != 'Cancel Purchase' and row.trn.types != 'Cancel Sales':
			# val=val+row.billQty
			if row.trn.types == 'Purchase':
				val=val+row.billQty
			if row.trn.types == 'Sales':
				val=val-row.billQty

			record=[row.trn.trn,row.trn.types,row.trn.baseproduct,row.invoiceDate,row.invoiceNumber,row.trn.client,
			row.trn.ratePMT,row.trn.incoterm,row.billQty,float(row.trn.ratePMT)*float(row.billQty),row.billNumber,
			row.billDate,row.logisticAgent,row.liner,row.etd,row.eta,val]

			row_num += 1
		else:
			val=0
			record=['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-']
			row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def GetRate(request):
	types=request.POST['type']
	product=request.POST['product']

	pro=cost.Inventory.objects.get(product=product,category=types)
	print(pro.product,pro.rate,pro.qty)
	return JsonResponse({'qty':pro.qty})
