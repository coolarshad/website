# from home.models import TradeApproval,PrePayments,SalesAndPurchase,ExtraCost,PL,PaymentAndFinance,Disputes

def PurchseInvoiceAmount(i):
	t=TradeApproval.objects.get(pk=i)
	s=SalesAndPurchase.objects.get(pk=i)
