from costmanagement.models import *
import json
from django.forms.models import model_to_dict

def GetConsumption(product,netBlendingQty):
	obj1=Consumption.objects.get(product=product)
	additives=[]
	oils=[]

	try:
		for i in obj1.consumptionadditive_set.all():
			percent=i.QtyInPercent
			liter=float(percent/100)*float(netBlendingQty)
			cost=AllAdditives.objects.get(product=i.name).costPriceInLiter
			print(cost)
			value=liter*cost
			obj=ConsumptionAdditive.objects.create(name=i.name,QtyInPercent=percent,QtyInLiters=liter,value=value)
			obj=model_to_dict(obj)
			additives.append(obj)
			print(str(additives)+'additives')
	except Exception as e:
		print(str(e)+'additives')

	try:
		for i in obj1.consumptionbaseoil_set.all():
			percent=i.QtyInPercent
			liter=float(percent/100)*float(netBlendingQty)
			cost=RawMaterials.objects.get(product=i.name).costPerLiter
			value=liter*cost
			obj=ConsumptionBaseOil.objects.create(name=i.name,QtyInPercent=percent,QtyInLiters=liter,value=value)
			obj=model_to_dict(obj)
			oils.append(obj)
			print(str(oils)+" oils")
	except Exception as e:
		print(str(e)+'oils')

	return (additives,oils)
	