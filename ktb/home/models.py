from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
import datetime

# # Create your models here.
class TradeApproval(models.Model):
	sn=models.IntegerField()
	
	company=models.CharField(max_length=255)
	# p_company=models.CharField(max_length=255)
	trd=models.CharField(max_length=255)
	# p_trd=models.DateField(blank=True, null=True)
	trn=models.CharField(max_length=255)
	# p_trn=models.CharField(max_length=255)
	types=models.CharField(max_length=255)
	# p_type=models.CharField(max_length=255)
	product=models.CharField(max_length=255)
	baseproduct=models.CharField(max_length=255,null=True,blank=True)
	# p_product=models.CharField(max_length=255)
	origin=models.CharField(max_length=255)
	# p_origin=models.CharField(max_length=255)
	client=models.CharField(max_length=255)   
	# p_supplier=models.CharField(max_length=255)
	address=models.TextField()
	# p_address=models.CharField(max_length=255)
	tad=models.CharField(max_length=255)
	# p_tad=models.DateField(blank=True, null=True)
	trade_status=models.CharField(max_length=255)
	# p_trade_status=models.CharField(max_length=255)
	tcq=models.CharField(max_length=255)
	contractUnit=models.CharField(max_length=255)
	# p_tcq=models.CharField(max_length=255)
	tolerance=models.CharField(max_length=255)
	# p_tolerance=models.CharField(max_length=255)
	packing=models.CharField(max_length=255)
	# p_packing=models.CharField(max_length=255)
	tuq = models.CharField(max_length=255)
	tuqUnit = models.CharField(max_length=255)

	contractBalanceQty = models.CharField(max_length=255)
	contractBalanceUnit = models.CharField(max_length=255)
	# p_tuq = models.CharField(max_length=255)
	ratePMT = models.CharField(max_length=255)
	
	commissionAgent=models.CharField(max_length=255)
	# p_commissionAgent=models.CharField(max_length=255)
	commissionRate= models.CharField(max_length=255)
	
	logisticProvider=models.CharField(max_length=255)
	# p_logisticProvider=models.CharField(max_length=255)
	estimatedLogisticsCost=models.CharField(max_length=255)
	
	paymentTerm=models.CharField(max_length=255)
	# p_paymentTerm=models.CharField(max_length=255)
	incoterm=models.CharField(max_length=255)
	# p_incoterm=models.CharField(max_length=255)
	pol=models.CharField(max_length=255)
	pod=models.CharField(max_length=255)
	# p_pol=models.CharField(max_length=255)
	etd=models.CharField(max_length=255)
	# p_etd=models.DateField(blank=True, null=True)
	eta=models.CharField(max_length=255)
	remarks=models.TextField()
	# p_eta=models.DateField(blank=True, null=True)
	po_number=models.CharField(max_length=255,blank=True, null=True)
	po_date=models.CharField(max_length=255,blank=True, null=True)
	so_number=models.CharField(max_length=255,blank=True, null=True)
	so_date=models.CharField(max_length=255,blank=True, null=True)

	manager1=models.CharField(max_length=255,blank=True, null=True)
	manager2=models.CharField(max_length=255,blank=True, null=True)
	approve1=models.BooleanField()
	approve2=models.BooleanField()
	approve1date=models.CharField(max_length=255,blank=True, null=True)
	approve2date=models.CharField(max_length=255,blank=True, null=True)

	bank=models.CharField(max_length=255,null=True,blank=True)
	account=models.CharField(max_length=255,null=True,blank=True)
	swift=models.CharField(max_length=255,null=True,blank=True)

	def __str__(self):
		return self.trn
		
# @receiver(pre_save, sender=TradeApproval)
# def update_product_trace(sender, instance, **kwargs):
# 	types=instance.types
# 	product=instance.product
# 	trn=TradeApproval.objects.get(trn=instance.trn)
# 	if types == 'Cancel Purchase':
# 		#if float(trn.tcq) != float(instance.tcq) and float(trn.tuq) != float(instance.tuq):
# 		if trn.types != 'Cancel Purchase':
# 			if PurchaseProductTrace.objects.filter(product=product).exists():
# 				pro=PurchaseProductTrace.objects.get(product=product)
# 			# print(pro.tbq,pro.tuq,instance.tuq)
# 				pro.tbq=float(pro.tbq)+float(instance.tuq)
# 				pro.save()
# 	if types == 'Cancel Sales':
# 		if float(trn.tcq) != float(instance.tcq) and float(trn.tuq) != float(instance.tuq):
# 			if SalesProductTrace.objects.filter(product=product).exists():
# 				pro=SalesProductTrace.objects.get(product=product)
# 			# print(pro.tbq,pro.tuq,instance.tuq)
# 				pro.tbq=float(pro.tbq)+float(instance.tuq)
# 				pro.save()
	# print(instance.types, instance.product)

# @receiver(pre_save, sender=TradeApproval)
# def update_product_qty(sender, instance, **kwargs):
# 	types=instance.types
# 	product=instance.product
# 	if TradeApproval.objects.filter(trn=instance.trn):
# 		trn=TradeApproval.objects.get(trn=instance.trn)
# 	else:
# 		trn=None
# 	if types == 'Purchase' or types == 'Purchase Amendment':
# 		if PurchaseProductTrace.objects.filter(product=product).exists():
# 			pro=PurchaseProductTrace.objects.get(product=product)
# 			if float(pro.tcq) != float(instance.tcq) and instance.tcq != '0':
# 				rem=float(instance.tcq)-float(pro.tcq)
# 				pro.tcq=float(instance.tcq)
				
# 				diff=float(instance.tuq)-float(trn.tuq)
# 				pro.tbq=float(pro.tbq)+rem-diff
# 				# pro.tuq=instance.tuq#could be some issue
# 				pro.save()
# 			if float(pro.tcq)== float(instance.tcq):
# 				if trn != None:
# 					if float(trn.tuq) != float(instance.tuq) and float(instance.tuq) <= float(pro.tbq):
# 					# pro.tuq=float(instance.tuq)
# 						rem=float(instance.tuq)-float(trn.tuq)
# 					# print(pro.tbq,rem)
# 						pro.tbq=float(pro.tbq)-rem
# 					# print(pro.tbq,rem)
# 						pro.save()
# 				else:
# 					pass

# 	if types == 'Sales' or types == 'Sales Amendment':
# 		if SalesProductTrace.objects.filter(product=product).exists():
# 			pro=SalesProductTrace.objects.get(product=product)
# 			if float(pro.tcq) != float(instance.tcq) and instance.tcq != '0':
# 				rem=float(instance.tcq)-float(pro.tcq)
# 				pro.tcq=float(instance.tcq)
# 				diff=float(instance.tuq)-float(trn.tuq)
# 				pro.tbq=float(pro.tbq)+rem-diff
# 				# pro.tbq=float(pro.tbq)+rem
# 				# pro.tuq=float(instance.tuq)
# 				pro.save()
# 			if float(pro.tcq) == float(instance.tcq):
# 				if trn != None:
# 					if float(trn.tuq) != float(instance.tuq) and float(instance.tuq) <= float(pro.tbq):
# 					# pro.tuq=float(instance.tuq)
# 						rem=float(instance.tuq)-float(trn.tuq)
# 						pro.tbq=float(pro.tbq)-rem
# 						pro.save()
# 				else:
# 					pass

class PurchaseProductTrace(models.Model):
	product=models.CharField(max_length=255)
	tcq=models.FloatField(null=True)
	tuq=models.FloatField(null=True)
	tbq=models.FloatField(null=True)
	first_trn=models.CharField(max_length=255,null=True,blank=True)
	def __str__(self):
		return self.product 

class SalesProductTrace(models.Model):
	product=models.CharField(max_length=255)
	tcq=models.FloatField(null=True)
	tuq=models.FloatField(null=True)
	tbq=models.FloatField(null=True)
	first_trn=models.CharField(max_length=255,null=True,blank=True)
	def __str__(self):
		return self.product

class PrePayments(models.Model):
	trn=models.OneToOneField(TradeApproval,on_delete=models.CASCADE)
	dueDate=models.CharField(max_length=255)
	# p_dueDate=models.DateField(blank=True,null=True)
	advance=models.FloatField()
	# s_advanceCur=models.CharField(max_length=255,blank=True)
	# p_advance=models.FloatField()
	# p_advanceCur=models.CharField(max_length=255,blank=True)
	lcNumberValue=models.CharField(max_length=255)
	# p_lcNumberValue=models.CharField(max_length=255)
	lcIssuingBank=models.CharField(max_length=255)
	# p_lcIssuingBank=models.CharField(max_length=255)
	advanceFromBuyers=models.FloatField(blank=True,null=True)
	# advnaceBuyCur=models.CharField(max_length=255,blank=True)
	advanceToSellers=models.FloatField(blank=True,null=True)
	# advnaceSellCur=models.CharField(max_length=255,blank=True)
	receivedDate=models.CharField(max_length=255,blank=True,null=True)
	paidDate=models.CharField(max_length=255,blank=True,null=True)
	lcExpiryDate=models.CharField(max_length=255,blank=True,null=True)
	nextShipmentDate=models.CharField(max_length=255,blank=True,null=True)
	# p_lcExpiryDate=models.DateField(blank=True,null=True)
	remarks=models.TextField(null=True,blank=True)
	def __str__(self):
		return str(self.advanceFromBuyers)


class SalesAndPurchase(models.Model):
	trn=models.OneToOneField(TradeApproval,on_delete=models.CASCADE,primary_key=True)
	invoiceDate=models.CharField(max_length=255, blank=True, null=True)
	
	invoiceNumber=models.CharField(max_length=255)
	
	invoiceAmount=models.FloatField() #TradeApproval(p_ratePMT) * purchaseBillQty
	
	commissionAgent=models.CharField(max_length=255)#TradeApproval(p_commissionAgent)
	
	commissionAmount=models.FloatField()#TradeApproval(p_commissionRate) * purchaseBillQty
	
	packingListDetails=models.CharField(max_length=255)
	
	billNumber=models.CharField(max_length=255)
	# salesBillNumber=models.CharField(max_length=255)
	billQty=models.FloatField()
	# salesBillQty=models.FloatField()
	billDate=models.CharField(max_length=255, blank=True, null=True)
	# salesBillDate=models.DateField()
	logisticAgent=models.CharField(max_length=255)
	# salesLogisticAgent=models.CharField(max_length=255)
	logisticCost=models.FloatField()
	
	liner=models.CharField(max_length=255)
	eta=models.CharField(max_length=255, blank=True, null=True)
	etd=models.CharField(max_length=255, blank=True, null=True)
	
	shipmentStatus=models.CharField(max_length=255)
	remarks=models.TextField(null=True,blank=True)
	reviewed=models.NullBooleanField(blank=True)
	batch_no=models.CharField(null=True,blank=True,max_length=100)
	production_date=models.CharField(max_length=255, blank=True, null=True)
	
	def __str__(self):
		  	return self.shipmentStatus

class ExtraCost(models.Model):
	trn=models.OneToOneField(TradeApproval,on_delete=models.CASCADE,primary_key=True)
	bankCharges=models.FloatField()
	
	billFee=models.FloatField()
	
	billCollectionCharges=models.FloatField()
	
	otherCharges=models.FloatField()
	remarks=models.TextField(null=True,blank=True)


	def __str__(self):
		return str(self.bankCharges)

class PaymentAndFinance(models.Model):
	trn=models.OneToOneField(TradeApproval,on_delete=models.CASCADE,primary_key=True)
	balancePayment=models.FloatField(blank=True,null=True)#SalesAndPurchase(salesInvoiceAmount)-PrePayments(advanceFromBuyers)
	
	dueDate=models.CharField(max_length=255,blank=True,null=True)
	# supplierDueDate=models.DateField()
	payment=models.FloatField(blank=True,null=True)
	
	paymentDate=models.CharField(max_length=255,blank=True,null=True)
	# p_paymentDate=models.DateField()
	balanceDue=models.FloatField(blank=True,null=True)		# balancePaymentFromBuyer - paymentReceived
	
	paymentMode=models.CharField(max_length=255)
	# p_paymentMode=models.CharField(max_length=255)
	paymentStatus=models.CharField(max_length=255)
	# p_paymentStatus=models.CharField(max_length=255)
	logisticsPaymentDue=models.FloatField(blank=True,null=True)	#SalesAndPurchase(salesLogisticCost)
	logisticsProvider=models.CharField(max_length=255)
	commissionAgent=models.CharField(max_length=255)
	
	logisticsCommissionDueDate=models.CharField(max_length=255,blank=True,null=True)
	agentCommissionDueDate=models.CharField(max_length=255,blank=True,null=True)
	
	agentCommissionPaid=models.FloatField(blank=True,null=True)
	remarks=models.TextField(null=True,blank=True)

	def __str__(self):
		return self.paymentStatus


class Disputes(models.Model):
	trn=models.OneToOneField(TradeApproval,on_delete=models.CASCADE,primary_key=True)
	dispute=models.CharField(max_length=255)
	# p_dispute=models.CharField(max_length=255)
	remark=models.TextField()
	# remark=models.CharField(max_length=255)

	def __str__(self):
		return self.s_remark


class PL(models.Model):
	trn=models.OneToOneField(TradeApproval,on_delete=models.CASCADE,primary_key=True) 
	p_trn=models.CharField(max_length=255)
	s_purchaseTotalCost=models.FloatField()	#SalesAndPurchase(salesCommissionAmount) + SalesAndPurchase(salesLogisticCost) + ExtraCost(s_bankCharges) + ExtraCost(salesBillFee) + ExtraCost(s_billCollectionCharges) + ExtraCost(s_otherCharges)
	p_purchaseTotalCost=models.FloatField()	#SalesAndPurchase(purchaseInvoiceAmount) + SalesAndPurchase(purchaseCommissionAmount) + SalesAndPurchase(purchaseLogisticCost) + ExtraCost(p_bankCharges) + ExtraCost(purchaseBillFee) + ExtraCost(p_billCollectionCharges) + ExtraCost(p_otherCharges)
	totalRevenueFromSales=models.FloatField()	#SalesAndPurchase(salesInvoiceAmount) 
	grossProfit=models.FloatField()			#totalRevenuefromSales - (p_purchaseTotalCost + s_purchaseTotalCost)
	profitPerDrum=models.FloatField()		#grossProfit / SalesAndPurchase(purchaseBillQty)
	remarks=models.TextField(null=True,blank=True)
	def __str__(self):
		return str(self.grossProfit)



class SnCount(models.Model):
	sn=models.IntegerField(primary_key=True)

	def __str__(self):
		return str(self.sn)
		
class TradeRefNo(models.Model):
	kp=models.IntegerField()
	sl=models.IntegerField()

	def __str__(self):
		return str(self.kp)		

class Kyc(models.Model):
	date=models.CharField(max_length=255)
	name=models.CharField(max_length=255)
	companyRegNo=models.CharField(max_length=255)
	regAddress=models.CharField(max_length=255)
	mailingAddress=models.CharField(max_length=255)
	telephone=models.CharField(max_length=255)
	fax=models.CharField(max_length=255)
	person1=models.CharField(max_length=255)
	designation1=models.CharField(max_length=255)
	mobile1=models.CharField(max_length=255)
	email1=models.CharField(max_length=255)
	person2=models.CharField(max_length=255)
	designation2=models.CharField(max_length=255)
	mobile2=models.CharField(max_length=255)
	email2=models.CharField(max_length=255)
	banker=models.CharField(max_length=255, null=True,blank=True)
	address=models.CharField(max_length=255, null=True,blank=True)
	swiftCode=models.CharField(max_length=255, null=True,blank=True)
	accountNumber=models.CharField(max_length=255, null=True,blank=True)
	approve1=models.BooleanField(default=False)
	approve2=models.BooleanField(default=False)
	def __str__(self):
		return self.name

class InventorySn(models.Model):
	sn=models.IntegerField(primary_key=True)

	def __str__(self):
		return str(self.sn)

class SaveInventory(models.Model):
	"""docstring for SaveInventory"""
	sn=models.IntegerField()
	entrydate=models.CharField(max_length=255)
	godowndate=models.CharField(max_length=255)
	trn=models.CharField(max_length=255)
	product=models.CharField(max_length=255)
	trd=models.CharField(max_length=255)
	supplier=models.CharField(max_length=255)
	qtyin=models.FloatField()
	qtyout=models.FloatField()
	incoterm=models.CharField(max_length=255)
	expense=models.FloatField()
	# expenseCur=models.CharField(max_length=255)
	net=models.FloatField()
	# netCur=models.CharField(max_length=100)
	oldbalqtyvalue=models.FloatField()
	balanceqty=models.FloatField()
	unit=models.CharField(max_length=255)
	godownlocation=models.CharField(max_length=255)
	oldinventoryvalue=models.FloatField()
	inventoryvalue=models.FloatField()
	currentinventoryrate=models.FloatField()
	def __str__(self):
		return self.product

class Products(models.Model):
	name=models.CharField(max_length=255)
	balanceqty=models.FloatField()
	unit=models.CharField(max_length=100)
	inventoryvalue=models.FloatField()
	inventoryrate=models.FloatField()

	def __str__(self):
		return self.name


class SnStock(models.Model):
	sn=models.IntegerField(primary_key=True)

	def __str__(self):
		return (str(self.sn))

class StockNo(models.Model):
	number=models.IntegerField(primary_key=True)

	def __str__(self):
		return str(self.number)

class StockJournal(models.Model):
	# sn=models.IntegerField()
	stockno=models.IntegerField()
	stockdate=models.CharField(max_length=255)
	
	product=models.CharField(max_length=255)
	qty=models.FloatField()
	unit=models.CharField(max_length=255)
	value=models.FloatField()
	rate=models.FloatField()
	production_remarks=models.CharField(max_length=255)
	consumption_remarks=models.CharField(max_length=255)

	def __str__(self):
		return self.product

class StockRaw(models.Model):
	product=models.ForeignKey(StockJournal,on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=255)
	qtykg=models.FloatField()
	density=models.FloatField()
	qtyliter=models.FloatField()
	ratekg=models.FloatField()
	valuekg=models.FloatField()
	rateliter=models.FloatField()
	valueliter=models.FloatField()

	def __str__(self):
		return self.name

class StockAdditive(models.Model):
	product=models.ForeignKey(StockJournal,on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=255)
	qtykg=models.FloatField()
	density=models.FloatField()
	qtyliter=models.FloatField()
	ratekg=models.FloatField()
	valuekg=models.FloatField()
	rateliter=models.FloatField()
	valueliter=models.FloatField()

	def __str__(self):
		return self.name

class StockPacking(models.Model):
	product=models.ForeignKey(StockJournal,on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=255)
	qty=models.FloatField()
	unit=models.CharField(max_length=255)
	rate=models.FloatField()
	value=models.FloatField()
	

	def __str__(self):
		return self.name
class StockConsumption(models.Model):
	product=models.ForeignKey(StockJournal,on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=255)
	qty=models.FloatField()
	unit=models.CharField(max_length=255)
	rate=models.FloatField()
	value=models.FloatField()
	

	def __str__(self):
		return self.name

class Log(models.Model):
	logdate=models.DateTimeField()
	user=models.CharField(max_length=255)
	authority=models.CharField(max_length=255)
	action=models.CharField(max_length=255)

	class Meta:
		ordering=('-logdate',)

	def __str__(self):
		return self.action
