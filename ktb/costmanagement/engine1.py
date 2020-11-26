from costmanagement.models import *
import json
from django.forms.models import model_to_dict

def GetAllAdditive(product,netBlendingQtyLiter):
	obj1=AllAdditives.objects.get(product=product)
	obj2=Additive.objects.get(product=product)

	polymers=[]
	oils=[]
	costs=[]
	try:
		for i in obj2.additivespolymer_set.all():
			percent=i.qtyInPercent
			liters=float(percent/100)*float(netBlendingQtyLiter)
			density=RawMaterials.objects.get(product=i.name).density
			kgs=float(liters*density)
			obj=AdditivesPolymer.objects.create(name=i.name,qtyInPercent=percent,qtyInLiters=liters,density=density,qtyInKgs=kgs)
			obj=model_to_dict(obj)
			# print(obj)
			polymers.append(obj)
	except Exception as e:
		print(str(e)+'poly')

	try:
		for i in obj2.additivesbaseoil_set.all():
			percent=i.qtyInPercent
			liters=float(percent/100)*float(netBlendingQtyLiter)
			density=RawMaterials.objects.get(product=i.name).density
			kgs=float(liters*density)
			obj=AdditivesBaseOil.objects.create(name=i.name,qtyInPercent=percent,qtyInLiters=liters,density=density,qtyInKgs=kgs)
			obj=model_to_dict(obj)
			# print(obj)
			oils.append(obj)
	except Exception as e:
		print(str(e)+' oils')

	try:
		rate=0
		cost=0
		net=0
		for i in obj2.additivesraw_set.all():
			product=i.product
			
			importRate=float(i.importRate)
			rate=rate+importRate
			addCost=i.addCost
			cost=cost+addCost
			total=float(importRate+addCost)
			
			density=RawMaterials.objects.get(product=product).density
			
			mtToKl=float(total*density)
			
			usage=i.usage
			netCost=float((usage/100)*mtToKl)
			
			net=float(net)+float(netCost)
			
			
		obj=AllAdditives.objects.create(sn=1,product=product,crfPrice=importRate,addCost=addCost,
				costPriceInLiter=float(net/1000),density=density,totalCost=float(rate+cost))
		print(obj)
		obj=model_to_dict(obj)
		print(obj)
		costs.append(obj)
	except Exception as e:
		print(str(e)+' raw')


	return (polymers,oils,costs)