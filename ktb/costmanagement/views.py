from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from costmanagement.models import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import xlwt 
from home.logs import *
import calendar
# Create your views here.

def Raw(request):
	try:
		obj=RawMaterials.objects.all().order_by('product')
		msgs=Log.objects.all()[:50]
	except Exception as e:
		obj=None

	cxt={'records':obj,'msgs':msgs}
	return render(request,'rawmaterials.html',context=cxt)
def ApproveRaw(request):
	product=request.POST['product']
	try:
		if RawMaterials.objects.filter(product=product).exists():
			raw=RawMaterials.objects.get(product=product)
			raw.approved=True
			raw.save()
			Logging(request,"Raw materials Approved of "+raw.product)
	except Exception as e:
		print(e)
	return redirect('costmanagement:raw')

def SaveRaw(request):
	try:
		if not RawMaterials.objects.filter(product=request.POST['rawmaterialproduct-input']):
			obj=RawMaterials.objects.create(product=request.POST['rawmaterialproduct-input'],
			costPerLiter=request.POST['rawmaterial_perlitercost-input'],buyPricePmt=request.POST['rawmaterial_buypricepmt-input'],
			addCost=request.POST['rawmaterial_addcost-input'],total=request.POST['rawmaterial_total-input'],
			mlToKl=request.POST['rawmaterial_mttokl-input'],density=request.POST['rawmaterial_density-input'],remarks=request.POST['rawmaterial-remarks'])
			obj.save()
			Logging(request,'Raw Materials details saved '+obj.product)
	except Exception as e:
		print(e)

	return redirect('costmanagement:raw')

def EditRaw(request):
	try:
		print('editing')
		if RawMaterials.objects.filter(product=request.POST['rawmaterialproduct-input']).exists():
			obj=RawMaterials.objects.get(product=request.POST['rawmaterialproduct-input'])
			obj.product=request.POST['rawmaterialproduct-input']
			obj.costPerLiter=request.POST['rawmaterial_perlitercost-input']
			obj.buyPricePmt=request.POST['rawmaterial_buypricepmt-input']
			obj.addCost=request.POST['rawmaterial_addcost-input']
			obj.total=request.POST['rawmaterial_total-input']
			obj.mlToKl=request.POST['rawmaterial_mttokl-input']
			obj.density=request.POST['rawmaterial_density-input']
			obj.remarks=request.POST['rawmaterial-remarks']
			obj.save()
			# messages.success(request, 'Raw Materials was edited successfully!')
			Logging(request,'Raw Materials details edited '+obj.product)
		# obj=RawMaterials.objects.filter(product=request.POST['rawmaterialproduct-input']).update(
		# 	costPerLiter=request.POST['rawmaterial_perlitercost-input'],buyPricePmt=request.POST['rawmaterial_buypricepmt-input'],
		# 	addCost=request.POST['rawmaterial_addcost-input'],total=request.POST['rawmaterial_total-input'],
		# 	mlToKl=request.POST['rawmaterial_mttokl-input'],density=request.POST['rawmaterial_density-input'])
		# obj.save()
		print('edited')
	except Exception as e:
		print(e)
	return redirect('costmanagement:raw')

def Additives(request):
	try:
		records=AllAdditives.objects.all()
		msgs=Log.objects.all()[:50]
	except Exception as e:
		records=None

	return render(request,'additives.html',context={'records':records,'msgs':msgs})

def SaveAdditives(request):
	# rawcount=request.POST['count-raw']
	# polymercount=request.POST['count-polymer']
	# oilcount=request.POST['count-polymer']
	# try:
	# 	print('additive')
	# 	# obj=Additive.objects.create(date=request.POST['additivesformation_date-input'],
	# 	obj=Additive.objects.create(date=request.POST['additivesformation_date-input'],
	# 		product=request.POST['additivesformationproductname-input'],netBlendingQtyLiter=request.POST['additivesformation_netblendingqnty_liter-input'],
	# 		grossVolCrosscheck=request.POST['additivesformation_grossvol_crosscheck-input'],percentCrosscheck=request.POST['additivesformation_percent_crosscheck-input'])
	# 	obj.save()
	# 	print('additive done')
	# except Exception as e:
	# 	print(e)
	# for i in range(1,int(rawcount)+1):
	# 	print(i)
	# 	try:
	# 		print('raw')
	# 		raw=AdditivesRaw.objects.create(additive=obj,
	# 			product=request.POST['additivesformationproduct-input'+str(i)],importRate=request.POST['additivesformation_importrate-input'+str(i)],
	# 			addCost=request.POST['additivesformation_addcost-input'+str(i)],total=request.POST['additivesformation_total-input'+str(i)],
	# 			mtToKl=request.POST['additivesformation_mttokl-input'+str(i)],usage=request.POST['additivesformation_usage-input'+str(i)],
	# 			netCost=request.POST['additivesformation_netcost-input'+str(i)])
	# 		raw.save()
	# 		print('raw done')
	# 	except Exception as e:
	# 		print(e)

	# for j in range(1,int(polymercount)+1):
	# 	print(j)
	# 	try:
	# 		print('polymer')
	# 		polymer=AdditivesPolymer.objects.create(additive=obj,
	# 			name=request.POST['additivesformationpolymername-input'+str(j)],qtyInPercent=request.POST['additivesformationpolymer_percent-input'+str(j)],
	# 			qtyInLiters=request.POST['additivesquantity_liter-input'+str(j)],density=request.POST['additivesformationpolymer_density-input'+str(j)],
	# 			qtyInKgs=request.POST['additivesformationpolymer_kg-input'+str(j)])
	# 		polymer.save()
	# 		print('polymer done')
	# 	except Exception as e:
	# 		print(e)

	# for k in range(1,int(oilcount)+1):
	# 	try:
	# 		print('all additives')
	# 		oil=AdditivesBaseOil.objects.create(additive=obj,
	# 			name=request.POST['additivesformation_baseoilname-input'+str(k)],qtyInPercent=request.POST['additivesformation_baseoil_percent-input'+str(k)],
	# 			qtyInLiters=request.POST['additivesformation_baseoil_liter-input'+str(k)],density=request.POST['additivesformation_baseoil_density-input'+str(k)],
	# 			qtyInKgs=request.POST['additivesformation_baseoil_kgs-input'+str(k)])
	# 		oil.save()
	# 		print('all additive done')
	# 	except Exception as e:
	# 		print(e)

	try:
		if not AllAdditives.objects.filter(product=request.POST['additivesname-input']):
			add=AllAdditives.objects.create(
			product=request.POST['additivesname-input'],
			crfPrice=request.POST['additivescfrprice-input'],addCost=request.POST['additivesaddcosta-input'],
			costPriceInLiter=request.POST['additiveslitercost_price-input'],density=request.POST['additives_densityat15deg-input'],
			totalCost=request.POST['additives_totalcost_exdk-input'],remarks=request.POST['additives-remarks'])
			add.save()
			Logging(request,'Additive details saved for '+add.product)
	except Exception as e:
		print(e)

	return redirect('costmanagement:additives')
def EditAllAdditives(request):
	try:
		if AllAdditives.objects.filter(product=request.POST['additivesname-input']).exists():
			obj=AllAdditives.objects.filter(product=request.POST['additivesname-input']).update(crfPrice=request.POST['additivescfrprice-input'],addCost=request.POST['additivesaddcosta-input'],
			costPriceInLiter=request.POST['additiveslitercost_price-input'],density=request.POST['additives_densityat15deg-input'],
			totalCost=request.POST['additives_totalcost_exdk-input'],remarks=request.POST['additives-remarks'])
			print('edited additives')
			Logging(request,'Additive details edited for '+request.POST['additivesname-input'])
	except Exception as e:
		print(e)

	return redirect('costmanagement:additives')

def ApproveAdditive(request):
	product=request.POST['product']
	try:
		if AllAdditives.objects.filter(product=product).exists():
			obj=AllAdditives.objects.get(product=product)
			obj.approved=True
			obj.save()
			Logging(request,"Additives Approved of "+obj.product)
	except Exception as e:
		print(e)
	return redirect('costmanagement:additives')

def AdditivesView(request,product):
	additive=Additive.objects.get(product=product)
	print(additive)
	net=0
	usage=0
	try:
		raws=additive.additivesraw_set.all()
		for i in raws:
			net=net+i.netCost
			print(net)
			usage=usage+i.usage
			print(usage)
		per_liter=float(net/1000)
		polymers=additive.additivespolymer_set.all()
		oils=additive.additivesbaseoil_set.all()
		alladditive=AllAdditives.objects.get(product=product)
		msgs=Log.objects.all()[:50]
	except Exception as e:
		print(e)
		raws=None
		polymers=None
		oils=None

	return render(request,'additivesview.html',{'per_liter':per_liter,'net':net,'usage':usage,'additive':additive,'raws':raws,'polymers':polymers,'oils':oils,'alladditive':alladditive,'msgs':msgs})

def Blendings(request):
	try:
		obj=Blending.objects.all()
		msgs=Log.objects.all()[:50]
	except Exception as e:
		print(e)
	return render(request,'blendingcost.html',{'records':obj,'msgs':msgs})

def SaveBlending(request):
	additivecount=request.POST['count-additive']
	oilcount=request.POST['count-oil']

	try:
		print('blending')
		obj=Blending.objects.create(product=request.POST['blendingcost_productname-input'],
			grade=request.POST['blendingcost_grade-input'],sae=request.POST['blendingcost_iso-input'],
			percentCrosscheck=request.POST['blendingcost_crosscheck-input'],perLiterCost=request.POST['blendingcost_perlitercost-input'])
		obj.save()
		print('blending done')
	except Exception as e:
		print(e)

	for i in range(1,int(additivecount)+1):
		print(i)
		try:
			print('BlendingAdditive')
			additive=BlendingAdditive.objects.create(product=obj,
				name=request.POST['blendingcost_additivesname-input'+str(i)],
				QtyInPercent=request.POST['blendingcost_additivesquantity_percent-input'+str(i)],
				QtyInLiters=request.POST['blendingcost_additivesvalue-input'+str(i)])
			additive.save()
			print('BlendingAdditive done')
		except Exception as e:
			print(e)

	for j in range(1,int(oilcount)+1):
		print(j)
		try:
			print('BlendingOil oil')
			oil=BlendingBaseOil.objects.create(product=obj,
				name=request.POST['blendingcost_baseoilname-input'+str(j)],
				QtyInPercent=request.POST['blendingcost_baseoilquantity_percent-input'+str(j)],
				QtyInLiters=request.POST['blendingcost_baseoilsvalue-input'+str(j)])
			oil.save()
			print('BlendingOil done')
		except Exception as e:
			print(e)
	
	return redirect('costmanagement:blending')

def Consumptions(request):
	try:
		obj=Consumption.objects.all().order_by('sn')
		additives=AllAdditives.objects.all()
		raw=RawMaterials.objects.all()
		msgs=Log.objects.all()[:50]
	except Exception as e:
		print(e)
	try:
		sn=SnConsumptions.objects.latest('sn')
		sn=sn.sn+1
	except Exception as ex:
		sn=1
	return render(request,'consumption.html',{'records':obj,'additives':additives,'raw':raw,'sn':sn,'msgs':msgs})

def SaveConsumption(request):
	additivecount=request.POST['count-additive']
	oilcount=request.POST['count-oil']
	print(oilcount)

	try:
		print('consumption')
		if not Consumption.objects.filter(product=request.POST['consumption_productname-input']).exists():
			obj=Consumption.objects.create(sn=request.POST['consumption_sn'],date=request.POST['consumption_date-input'],product=request.POST['consumption_productname-input'],
				grade=request.POST['consumption_grade-input'],sae=request.POST['consumption_iso-input'],
				netBlendingQty=request.POST['consumption_netblendingqnty-input'],grossVolCrosscheck=request.POST['consumption_volcrosscheck-input'],
				crosscheck=request.POST['blendingcost_crosscheck-input'],perLiterCost=request.POST['blendingcost_perlitercost-input'],
				totalvalue=request.POST['blendingcost_totalvalue-input'],remarks=request.POST['blendingcost_remarks-input'])
			obj.save()
			print('consumption done')
		else:
			return redirect('costmanagement:consumption')
	except Exception as e:
		print(e)

	for i in range(1,int(additivecount)+1):
		print(i)
		try:
			print('ConsumptionAdditive')
			additive=ConsumptionAdditive.objects.create(product=obj,
				name=request.POST['cosmumption_additivesname-input'+str(i)],
				QtyInPercent=request.POST['cosmumption_additivesquantity_percent-input'+str(i)],
				QtyInLiters=request.POST['cosmumption_additivesquantity_liter-input'+str(i)],
				value=request.POST['blendingcost_additivesvalue-input'+str(i)])
			additive.save()
			print('ConsumptionAdditive done')
		except Exception as e:
			print(e)

	for j in range(1,int(oilcount)+1):
		print(j)
		try:
			print('Consumption oil')
			oil=ConsumptionBaseOil.objects.create(product=obj,
				name=request.POST['cosmumption_baseoilname-input'+str(j)],
				QtyInPercent=request.POST['cosmumption_baseoilquantity_percent-input'+str(j)],
				QtyInLiters=request.POST['cosmumption_baseoilquantity_liter-input'+str(j)],
				value=request.POST['blendingcost_baseoilsvalue-input'+str(j)])
			oil.save()
			print('Consumption done')
		except Exception as e:
			print(e)
	Logging(request,'Consumption and Blending details saved for '+request.POST['consumption_productname-input'])
	try:
		sn=request.POST['consumption_sn']
		s=SnConsumptions.objects.create(sn=int(sn))
		s.save()
	except Exception as e:
		pass
	
	return redirect('costmanagement:consumption')

def BlendingView(request,product):
	product=Blending.objects.get(product=product)
	msgs=Log.objects.all()[:50]
	try:
		additives=product.blendingadditive_set.all()
		oils=product.blendingbaseoil_set.all()
	except:
		additives=None
		oils=None
	return render(request,'blendingcostview.html',{'additives':additives,'oils':oils,'product':product,'msgs':msgs})

def ConsumptionView(request,product):
	print(product)
	product=Consumption.objects.get(product=product)
	msgs=Log.objects.all()[:50]

	try:
		additives=product.consumptionadditive_set.all()
		oils=product.consumptionbaseoil_set.all()
		print(oils)
	except:
		additives=None
		oils=None
	return render(request,'consumptionview.html',{'additives':additives,'oils':oils,'product':product,'msgs':msgs})

def ApproveConsumption(request):
        product=request.POST['product']
        try:
                if Consumption.objects.filter(product=product).exists():
                        obj=Consumption.objects.get(product=product)
                        obj.approved=True
                        obj.save()
                        Logging(request,"Consumption and blending Approved of "+obj.product)
        except Exception as e:
                print(e)
        return redirect('costmanagement:consumption')

def FinalProducts(request):
	# try:
	# 	sn=SnFinalProduct.objects.latest('sn')
	# 	sn=sn.sn+1
	# except:
	# 	sn=1

	try:
		obj=FinalProduct.objects.all().order_by('sn')
		products=Consumption.objects.all()
		packing=Packing.objects.all()
		msgs=Log.objects.all()[:50]
	except:
		obj=None

	
	try:
		sn=SnFinalProduct.objects.latest('sn')
		sn=sn.sn+1
	except Exception as e:
		sn=1

	return render(request,'finalproductcost.html',{'records':obj,'products':products,'packing':packing,'sn':sn,'msgs':msgs})

def SaveFinalProduct(request):
	try:
		print('saving final product')
		obj=FinalProduct.objects.create(
			sn=request.POST['finalproduct_sn'],date=request.POST['finalproduct_date-input'],
			product=request.POST['finalproductname-input'],packingsize=request.POST['final_packingsize-input'],
			bottlesperpack=request.POST['final_bottles_perpack-input'],litersperpack=request.POST['final_liters_perpack-input'],
			totalqty=request.POST['final_totalquantity-text-input'],totalqtyunit=request.POST['final_totalquantity-input'],
			qtyinliters=request.POST['final_qtylitrs-input'],perlitercost=request.POST['final_perlitercost-input'],
			costpercase=request.POST['final_costpercasepail-input'],dkcost=request.POST['final_dkcost-input'],
			bottlepereac=request.POST['final_bottle-eac-input'],bottlepercase=request.POST['final_bottle-case-input'],
			lablepereac=request.POST['final_label-eac-input'],labelpercase=request.POST['final_label-case-input'],
			cartons=request.POST['final_cartons-input'],dkexprice=request.POST['final_dkexPrice-input'],
			kscost=request.POST['final_kscost-input'],totalsp=request.POST['final_sellingprice-input'],
			bottlecapprice=request.POST['final_price-bottlecap-input'],bottlecappercase=request.POST['final_bottlecap_per-case-input'],
			remarks=request.POST['final_remarks-input'])
		obj.save()
		print('product saved')

		sn=SnFinalProduct.objects.create(sn=request.POST['finalproduct_sn'])
		sn.save()
		Logging(request,'Final Product Cost details saved for '+obj.product)
		print('sn saved')
	except Exception as e:
		print(e)
	
	return redirect('costmanagement:finalproduct')

def EditFinalProduct(request):
	try:
		print('editing final product')

		obj=FinalProduct.objects.filter(sn=int(request.POST['finalproduct_sn'])).update(
			product=request.POST['finalproductname-input'],date=request.POST['finalproduct_date-input'],
			packingsize=request.POST['final_packingsize-input'],
			bottlesperpack=request.POST['final_bottles_perpack-input'],litersperpack=request.POST['final_liters_perpack-input'],
			totalqty=request.POST['final_totalquantity-text-input'],totalqtyunit=request.POST['final_totalquantity-input'],
			qtyinliters=request.POST['final_qtylitrs-input'],perlitercost=request.POST['final_perlitercost-input'],
			costpercase=request.POST['final_costpercasepail-input'],dkcost=request.POST['final_dkcost-input'],
			bottlepereac=request.POST['final_bottle-eac-input'],bottlepercase=request.POST['final_bottle-case-input'],
			lablepereac=request.POST['final_label-eac-input'],labelpercase=request.POST['final_label-case-input'],
			cartons=request.POST['final_cartons-input'],dkexprice=request.POST['final_dkexPrice-input'],
			kscost=request.POST['final_kscost-input'],totalsp=request.POST['final_sellingprice-input'],
			bottlecapprice=request.POST['final_price-bottlecap-input'],bottlecappercase=request.POST['final_bottlecap_per-case-input'],
			remarks=request.POST['final_remarks-input'])
		# obj.save()
		print('product edited')
		Logging(request,'Final Product Cost details edited for '+request.POST['finalproductname-input'])
		# sn=SnFinalProduct.objects.create(sn=request.POST['finalproductnum-input'])
		# sn.save()
		# print('sn saved')
	except Exception as e:
		print(e)
	
	return redirect('costmanagement:finalproduct')

def ApproveFinalProduct(request):
        sn=request.POST['sn']
        try:
                if FinalProduct.objects.filter(sn=sn).exists():
                        obj=FinalProduct.objects.get(sn=sn)
                        obj.approved=True
                        obj.save()
                        Logging(request,"Final Product Approved of "+obj.product)
        except Exception as e:
                print(e)
        return redirect('costmanagement:finalproduct')


@csrf_exempt
def EditConsumptions(request):
	sn=request.POST['sn']
	date=request.POST['date']
	product=request.POST['product']
	grade=request.POST['grade']
	sae=request.POST['sae']

	netBlendingQty=request.POST['netBlendingQty']
	netBlendingQty=float(netBlendingQty)

	grossVolCrosscheck=request.POST['grossVolCrosscheck']
	grossVolCrosscheck=float(grossVolCrosscheck)

	crosscheck=request.POST['crosscheck']
	crosscheck=float(crosscheck)

	totalvalue=request.POST['totalvalue']
	totalvalue=float(totalvalue)

	perLiterCost=request.POST['perLiterCost']
	perLiterCost=float(perLiterCost)
	remarks=request.POST['remarks']
	
	additives=json.loads(request.POST['additives'])
	oils=json.loads(request.POST['oils'])

	
	if Consumption.objects.filter(product=product).exists():
		obj=Consumption.objects.get(product=product)
		o=Consumption.objects.filter(product=product).update(sn=sn,date=date,grade=grade,sae=sae,
			netBlendingQty=netBlendingQty,grossVolCrosscheck=grossVolCrosscheck,
			crosscheck=crosscheck,perLiterCost=perLiterCost,
			totalvalue=totalvalue,remarks=remarks)
		# addset=obj.consumptionadditive_set.all()
		# for i,j in enumerate(addset):
		# 	add=ConsumptionAdditive.objects.filter(product=obj,name=j.name).update(
		# 		QtyInPercent=float(additives[i]['QtyInPercent']),
		# 		QtyInLiters=float(additives[i]['QtyInLiters']),
		# 		value=float(additives[i]['value']))
		if SnConsumptions.objects.filter(sn=int(sn)).exists():
			# sn=SnConsumptions.objects.get(sn=int(sn))
			pass
		else:
			SnConsumptions.objects.create(sn=int(sn))

		if ConsumptionAdditive.objects.filter(product=obj).exists():
			cset=ConsumptionAdditive.objects.filter(product=obj)
			for i,j in enumerate(cset):
				add=ConsumptionAdditive.objects.filter(product=obj,name=j.name).update(
				# name=additives[i]['name'],
				QtyInPercent=float(additives[i]['QtyInPercent']),
				QtyInLiters=float(additives[i]['QtyInLiters']),
				value=float(additives[i]['value']))
				

		if ConsumptionBaseOil.objects.filter(product=obj).exists():
			oset=ConsumptionBaseOil.objects.filter(product=obj)
			for i,j in enumerate(oset):
				add=ConsumptionBaseOil.objects.filter(product=obj,name=j.name).update(
				# name=oils[i]['name'],
				QtyInPercent=float(oils[i]['QtyInPercent']),
				QtyInLiters=float(oils[i]['QtyInLiters']),
				value=float(oils[i]['value']))
				
	Logging(request,'Consumption and Blending details edited for '+obj.product)
	return JsonResponse({'data':'ok'})

@csrf_exempt
def ExportInventoryForProduction(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Inventoryforproduction.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Inventoryforproduction')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Date','Category','Product','Quantity','Unit','Rate','Value']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()
	
		invs = Inventory.objects.all().order_by('category')

	for row in invs:
		
		record=[row.date,row.category,row.product,row.qty,row.unit,row.rate,row.value]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response


def InventoryList(request):
	try:
		raw=RawMaterials.objects.all()
		packing=Packing.objects.all()
		additives=AllAdditives.objects.all()
		consumptions=Consumption.objects.all()
		obj=Inventory.objects.all().order_by('category')
	except Exception as e:
		raw=RawMaterials.objects.all()
		packing=Packing.objects.all()
		additives=AllAdditives.objects.all()
		consumptions=Consumption.objects.all()
		obj=None
	try:
		sn=SnInventory.objects.latest('sn')
		sn=sn.sn+1
	except:
		sn=1
	
	msgs=Log.objects.all()[:50]
	return render(request,'costmanagement-inventory.html',{'records':obj,'sn':sn,'raw':raw,
		'packing':packing,'additives':additives,'consumptions':consumptions,'msgs':msgs})

def SaveInventory(request):
	try:
		print('saving inventory')
		
		count=int(request.POST['count'])
		# print(count)
		for i in range(count):
			# print(str(i))
			obj=Inventory.objects.create()
			obj.sn=int(request.POST['costinventory-sninput'])
			obj.date=request.POST['costinventorydate-input']
			obj.category=request.POST['costinventorycategory-input'+str(i+1)]
			obj.product=request.POST['costinventoryproduct-input'+str(i+1)]
			obj.qty=request.POST['costinventoryquantity-input'+str(i+1)]
			obj.unit=request.POST['costinventoryunits-input'+str(i+1)]
			obj.rate=request.POST['costinventoryrate-input'+str(i+1)]
			obj.value=request.POST['costinventory_value-input'+str(i+1)]
			obj.save()
			Logging(request,'Production Inventory added for'+obj.product)
		print('inventory saved')

		sn=SnInventory.objects.create(sn=request.POST['costinventory-sninput'])
		sn.save()

	except Exception as e:
		print(e)
	return redirect('costmanagement:inventory')

@csrf_exempt
def EditInvProduction(request):
	try:
		print('saving inventory')
		obj=Inventory.objects.get(product=request.POST['costinventoryproduct'])
		obj.sn=int(request.POST['costinventory-sninput'])
		obj.date=request.POST['costinventorydate-input']
		obj.category=request.POST['costinventorycategory']
			#obj.product=request.POST['costinventoryproduct-input'+str(i+1)]
		obj.qty=request.POST['costinventoryquantity-input']
		obj.unit=request.POST['costinventoryunits']
		obj.rate=request.POST['costinventoryrate-input']
		obj.value=request.POST['costinventory_value-input']
		obj.save()
		print('inventory saved')
		Logging(request,'Production Inventory edited for'+obj.product)
		
	except Exception as e:
		print(e)
	return redirect('costmanagement:inventory')

@csrf_exempt
def AlterInventory(request):
	product=request.POST['product']
	inventory=Inventory.objects.get(product=product)
	data={'sn':inventory.sn,'date':inventory.date,'category':inventory.category,
	'product':inventory.product,'qty':inventory.qty,'unit':inventory.unit,'rate':inventory.rate,
	'value':inventory.value}

	return JsonResponse(data)

@csrf_exempt
def DeleteInventory(request):
	product=request.POST['product']
	inventory=Inventory.objects.filter(product=product).delete()
	Logging(request,'Production Inventory deleted for'+product)
	return redirect("costmanagement:inventory")
def Packings(request):
	try:
		obj=Packing.objects.all().order_by('product')

	except Exception as e:
		obj=None
	msgs=Log.objects.all()[:50]
	try:
		sn=SnPacking.objects.latest('sn')
		sn=sn.sn+1
	except Exception as e:
		sn=1
	
	return render(request,'packing.html',{'records':obj,'sn':sn,'msgs':msgs})

def SavePacking(request):
	try:
		if not Packing.objects.filter(product=request.POST['packingproduct-input']):
			obj=Packing.objects.create(sn=request.POST['packing_sn'],date=request.POST['packing_date-input'],product=request.POST['packingproduct-input'],
			pereach=request.POST['packingpereach_price-input'],remarks=request.POST['packing-remarks'],category=request.POST['packingcategory'])
			obj.save()

			sn=SnPacking.objects.create(sn=request.POST['packing_sn'])
			sn.save()

			Logging(name,'Packing details saved '+request.POST['packingproduct-input'])
	except Exception as e:
		print(e)
	return redirect('costmanagement:packing')

def EditPacking(request):
	try:
		obj=Packing.objects.filter(product=request.POST['packingproduct-input']).update(
			sn=request.POST['packing_sn'],date=request.POST['packing_date-input'],
			pereach=request.POST['packingpereach_price-input'],remarks=request.POST['packing-remarks'],category=request.POST['packingcategory'])
		Logging(request,'Packing details edited '+request.POST['packingproduct-input'])
		# obj.save()
	except Exception as e:
		print(e)
	return redirect('costmanagement:packing')

def ApprovePacking(request):
        product=request.POST['product']
        print(product)
        try:
                if Packing.objects.filter(product=product).exists():
                        obj=Packing.objects.get(product=product)
                        obj.approved=True
                        obj.save()
                        Logging(request,"Packing Approved of "+obj.product)
        except Exception as e:
                print(e)
        return redirect('costmanagement:packing')

#---------------------------------------------------------------------
from . import engine1
from . import engine2
import json
from django.forms.models import model_to_dict

@csrf_exempt
def AlterRaw(request):
	try:
		# print("response")
		obj=RawMaterials.objects.get(product=request.POST['product'])
		print(obj)
		print("ok")
	except Exception as e:
		print(e)
		obj=None

	cxt={'product':obj.product,'costPerLiter':obj.costPerLiter,'buyPricePmt':obj.buyPricePmt,'addCost':obj.addCost,'total':obj.total,'mlToKl':obj.mlToKl,'density':obj.density,'remarks':obj.remarks,'approved':obj.approved}
	return JsonResponse(cxt)
@csrf_exempt
def AlterPacking(request):
	try:
		print("response")
		obj=Packing.objects.get(product=request.POST['product'])
		
		print("ok")
	except Exception as e:
		print(e)
		obj=None

	cxt={'sn':obj.sn,'date':obj.date,'product':obj.product,'pereach':obj.pereach,'category':obj.category,'remarks':obj.remarks,'approved':obj.approved}
	return JsonResponse(cxt)

@csrf_exempt
def DeletePacking(request):
	try:
		product=request.POST['product']
		obj=Packing.objects.filter(product=product).delete()
		Logging(request,'Packing details deleted '+product)
	except Exception as e:
		pass
	return redirect('costmanagement:packing')

@csrf_exempt
def DeleteRawMaterials(request):
	try:
		product=request.POST['product']
		obj=RawMaterials.objects.filter(product=product).delete()
		Logging(request,'Raw Materials details deleted '+product)
	except Exception as e:
		pass
	return redirect('costmanagement:raw')
	
@csrf_exempt
def GetAdditives(request):
	try:
		product=request.POST['product']
		netBlendingQtyLiter=request.POST['netBlendingQtyLiter']
		polymers,oils,costs=engine1.GetAllAdditive(product,netBlendingQtyLiter)
		# polymers=json.dumps(polymers)
		print(polymers)
		# oils=json.dumps(oils)
		print(oils)
		print(costs)
		# getadditive=engine1.GetAdditive(product)
		# getalladditive=AllAdditives.objects.get(product=product)
		# getadditive=Additive.objects.get(product=product)
		data={'polymers':polymers,'oils':oils,'costs':costs}
	except Exception as e:
		print(e)
		data={'polymers':None,'oils':None,'costs':None}
	return JsonResponse(data)


@csrf_exempt
def GetConsumption(request):
	try:
		product=request.POST['product']
		print(product)
		netBlendingQty=request.POST['netBlendingQty']
		# print()
		additives,oils=engine2.GetConsumption(product,netBlendingQty)
		
		print(additives)
		
		print(oils)
		
	
		data={'additives':additives,'oils':oils}
	except Exception as e:
		print(e)
		data={'additive':None,'oils':None}
	return JsonResponse(data)

@csrf_exempt
def GetFinalAll(request):
	try:
		product=request.POST['product']
		print(product)
		obj=Consumption.objects.get(product=product)
		obj=model_to_dict(obj)
		data={'product':obj}
	except Exception as e:
		print(e)
		data={'product':None}
	return JsonResponse(data)

@csrf_exempt
def GetFinal(request):
	try:
		product=request.POST['product']
		print(product)
		obj=FinalProduct.objects.get(sn=product)
		obj=model_to_dict(obj)
		data={'product':obj}
	except Exception as e:
		print(e)
		data={'product':None}
	return JsonResponse(data)

@csrf_exempt
def GetFinalProduct(request):
	try:
		product=request.POST['product']
		netQty=request.POST['totalQty']
		print(product+" "+netQty)
		obj=Consumption.objects.get(product=product)
		print(obj)
		additives,oils=engine2.GetConsumption(product,netQty)
		per_liter=0
		
		for i in additives:
			print()
			per_liter=per_liter+i['value']
	
		for i in oils:
			# print(i+'in views')
			per_liter=per_liter+i['value']
	
		# obj=model_to_dict(obj)
		data={'product':product,'totalQty':netQty,'perLiterCost':per_liter}
	except Exception as e:
		print(e)
		data={'product':None,'totalQty':None,'per_liter':None}
	return JsonResponse(data)

@csrf_exempt
def AlterAllAdditives(request):
	product=request.POST['product']
	additives=[]
	if AllAdditives.objects.filter(product=product).exists():
		obj=AllAdditives.objects.get(product=product)
		data={'product':obj.product,'crfPrice':obj.crfPrice,'addCost':obj.addCost,
		'costPriceInLiter':obj.costPriceInLiter,'density':obj.density,'totalCost':obj.totalCost,
		'remarks':obj.remarks,'approved':obj.approved}
	else:
		data=None
	return JsonResponse(data)

@csrf_exempt
def DeleteAdditives(request):
	product=request.POST['product']
	if AllAdditives.objects.filter(product=product).exists():
		obj=AllAdditives.objects.get(product=product).delete()
		Logging(request,'Additive details deleted for '+product)
	return redirect('costmanagement:additives')

@csrf_exempt
def DeleteConsumption(request):
 	product=request.POST['product']
 	print(product+" deleting")
 	if Consumption.objects.filter(product=product).exists():
 		obj=Consumption.objects.filter(product=product).delete()
 		#obj.save()
 		print('deleted')
 		Logging(request,'Consumption and blending details deleted for '+product)
 	return redirect('costmanagement:consumption')

@csrf_exempt
def DeleteFinal(request):
	product=request.POST['product']
	if FinalProduct.objects.filter(sn=product).exists():
		obj=FinalProduct.objects.get(sn=product)
		pro=obj.product
		obj.delete()
		Logging(request,'Final Product details deleted for '+pro)
	return redirect('costmanagement:finalproduct')	
@csrf_exempt
def FillAdditiveOil(request):
	name=request.POST['name']
	liters=request.POST['liters']
	types=request.POST['types']

	if types == 'additives':
		obj=AllAdditives.objects.get(product=name)
		price=(obj.costPriceInLiter*float(liters))
		data={'value':price}

	if types == 'oils':
		#if RawMaterials.objects.filter(product=name).exists():
		obj=RawMaterials.objects.get(product=name)
		price=(obj.costPerLiter*float(liters))
		data={'value':price}
		#else:
			#data={'value':0}
	return JsonResponse(data)

@csrf_exempt
def ExportRaw(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="RawMaterials.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Raw Materials Price')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Product Name','Cost Per Liter','Buy Price PMT','Add Cost','Total','ML to KL','Density','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()
	
		trns = RawMaterials.objects.filter(approved=True)

	for row in trns:
		
		record=[row.product,row.costPerLiter,row.buyPricePmt,row.addCost,row.total,row.mlToKl,row.density,row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportAdditives(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Additives.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Kyc')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Name of additives','CFR Price/KG in USD','Add Cost','Total cost EX DK in Kgs','Density @ 15 Degree Celsius','Cost Price in Liters','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()
	
		trns = AllAdditives.objects.filter(approved=True)

	for row in trns:
		
		record=[row.product,row.crfPrice,row.addCost,row.totalCost,row.density,row.costPriceInLiter,row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportConsumption(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Consumption&Blending.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('consumption')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['S.N','Blending Date','Product Name','Grade','SAE/ISO','Net Blending Quantity','Gross Vol.Check','Cross Check','Total Value','Per Liter Cost','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()
	
		trns = Consumption.objects.filter(approved=True).order_by('sn')

	for row in trns:
		
		record=[row.sn,row.date,row.product,row.grade,row.sae,row.netBlendingQty,row.grossVolCrosscheck,row.crosscheck,row.totalvalue,row.perLiterCost,row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response




@csrf_exempt
def ExportFinalProduct(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="FinalProducts.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('FinalProducts')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['S.N','DATE','PRODUCT NAME','PACKING SIZE','BOTTLES PER PACK','LITERS PER PACK','TOTAL QUANTITY','UNIT','QUANTITY IN LITERS','PER LITER COST',
	'COST PER CASE PAIL','DK COST','PRICE PER BOTTLE','BOTTLE PER CASE','PRICE PER BOTTLE CAP','BOTTLE CAP PER CASE','PRICE PER LABEL','LABEL PER CASE',
	'PRICE PER CARTON','DK EX-PRICE','KS COST','TOTAL SELLING PRICE','REMARKS']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()
	
		trns = FinalProduct.objects.filter(approved=True).order_by('sn')

	for row in trns:
		
		record=[row.sn,row.date,row.product,row.packingsize,row.bottlesperpack,row.litersperpack,row.totalqty,row.totalqtyunit,row.qtyinliters,row.perlitercost,row.costpercase,
		row.dkcost,row.bottlepereac,row.bottlepercase,row.bottlecapprice,row.bottlecappercase,row.lablepereac,row.labelpercase,
		row.cartons,row.dkexprice,row.kscost,row.totalsp,row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def ExportPacking(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Packings.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Kyc')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Product','Per each Price','Packing Category','Remarks']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()
	
		trns = Packing.objects.filter(approved=True)

	for row in trns:
		
		record=[row.product,row.pereach,row.category,row.remarks]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response


def RawConsumption(request):
	raws=[]
	densities=[]
	consumptions=Consumption.objects.all()
	msgs=Log.objects.all()[:50]
	for i in consumptions:
		raw=i.consumptionbaseoil_set.all()
		density=[]
		for a in raw:
			d=RawMaterials.objects.get(product=a.name).density
			density.append(d)
		raws.append(raw)
		densities.append(density)
		# print(densities)

	return render(request,"rawmaterialconsumption.html",{'products':consumptions,'raws':zip(raws,densities),'msgs':msgs})

def AdditivesConsumption(request):
	additives=[]
	densities=[]
	consumptions=Consumption.objects.all()
	msgs=Log.objects.all()[:50]
	for i in consumptions:
		additive=i.consumptionadditive_set.all()
		density=[]
		for a in additive:
			d=AllAdditives.objects.get(product=a.name).density
			density.append(d)
		additives.append(additive)
		densities.append(density)
	return render(request,"additiveconsumption.html",{'additives':zip(additives,densities),'msgs':msgs})


@csrf_exempt
def ExportRawConsumption(request):
	print('in here')
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="rawmaterialconsumption.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Raw Material Consumption')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Final Product Name','Raw Material Name','Date','S.N','Quantity in Kgs','Quantity in Ltrs','Rate/Ltr','Value']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	raws=[]
	consumptions=Consumption.objects.all()
	for i in consumptions:
		raw=i.consumptionbaseoil_set.all()
		raws.append(raw)

	# for row in raws:
	# print(raws)
	for i in raws:

		for j in i:
			d=RawMaterials.objects.get(product=j.name).density
			if j.value == 0 or j.QtyInLiters == 0:
				record=[j.product.product,j.name,j.product.date,j.product.sn,round((float(d)*float(j.QtyInLiters)),4),j.QtyInLiters,round(0,2),j.value]
			else:
				record=[j.product.product,j.name,j.product.date,j.product.sn,round((float(d)*float(j.QtyInLiters)),4),j.QtyInLiters,round(float(j.value/j.QtyInLiters),2),j.value]
			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response
	# return HttpResponse('Hi')


@csrf_exempt
def ExportAdditiveConsumption(request):
	print('in here')
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="additiveconsumption.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Additive Consumption')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Final Product Name','Additive Name','Date','S.N','Quantity in Kgs','Quantity in Ltrs','Rate/Ltr','Value']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	
	additives=[]
	consumptions=Consumption.objects.all()
	for i in consumptions:
		additive=i.consumptionadditive_set.all()
		additives.append(additive)
	for i in additives:
		
			# print(row.balanceDue)
			# pre.append(i)
		# for i in rows:
		for j in i:
			d=AllAdditives.objects.get(product=j.name).density
			if j.value == 0 or j.QtyInLiters == 0:
				record=[j.product.product,j.name,j.product.date,j.product.sn,float(d)*float(j.QtyInLiters),j.QtyInLiters,round(0,2),j.value]
			else:
				record=[j.product.product,j.name,j.product.date,j.product.sn,float(d)*float(j.QtyInLiters),j.QtyInLiters,round(float(j.value/j.QtyInLiters),2),j.value]
			row_num += 1
			for col_num in range(len(record)):
				ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response
	# return HttpResponse('Hi')

@csrf_exempt
def GetRate(request):
	category=request.POST['category']
	print(category)
	product=request.POST['product']
	print(product)

	if category == 'Raw Material':
		pro=RawMaterials.objects.get(product=product)

		return JsonResponse({'rate':pro.costPerLiter})
	if category == 'Additives':
		pro=AllAdditives.objects.get(product=product)

		return JsonResponse({'rate':pro.costPriceInLiter})
	if category == 'Packing Material':
		pro=Packing.objects.get(product=product)

		return JsonResponse({'rate':pro.pereach})
	if category == 'Consumption':
		pro=Consumption.objects.get(product=product)

		return JsonResponse({'rate':pro.perLiterCost})


@csrf_exempt
def ExportRawConsumptionFilter(request,year,month):

	year=year
	month=month
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]



	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="RawMaterialsConsumption.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('RawMaterialsConsumption')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Final Product Name','Raw Material Name','Date','S.N','Quantity in Kgs','Quantity in Ltrs','Rate/Ltr','Value']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	raws=[]
	consumptions = Consumption.objects.all().order_by('product')
	for i in consumptions:
		date1=datetime.strptime(i.date ,'%d/%m/%Y')
				
		d1=datetime(year,month,1)
		d2=datetime(year,month,days)
		
		if date1<d2 and date1>d1:
			raw=i.consumptionbaseoil_set.all()
			for j in raw:
				raws.append(j)

	for raw in raws:
		d=RawMaterials.objects.get(product=raw.name).density
		if raw.value != 0 and raw.QtyInLiters != 0:
			rate=float(raw.value)/float(raw.QtyInLiters)
		else:
			rate=0
		record=[raw.product.product,raw.name,raw.product.date,raw.product.sn,round((float(d)*float(raw.QtyInLiters)),4),round(raw.QtyInLiters,4),round(rate,4),round(raw.value,4)]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response


@csrf_exempt
def ExportAdditivesConsumptionFilter(request,year,month):

	year=year
	month=month
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]

	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="AdditivesMaterialsConsumption.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('AdditivesMaterialsConsumption')

    # Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	# columns = ['Final Product Name','Additive Name','Date','S.N','Quantity(Ltrs)','Rate','Value']
	columns = ['Final Product Name','Additive Name','Date','S.N','Quantity in Kgs','Quantity in Ltrs','Rate/Ltr','Value']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	font_style = xlwt.XFStyle()
	additives=[]
	consumptions = Consumption.objects.all().order_by('product')
	for i in consumptions:
		date1=datetime.strptime(i.date ,'%d/%m/%Y')
				
		d1=datetime(year,month,1)
		d2=datetime(year,month,days)
		
		if date1<d2 and date1>d1:
			additive=i.consumptionadditive_set.all()
			for j in additive:
				additives.append(j)

	for raw in additives:
		d=AllAdditives.objects.get(product=raw.name).density
		if raw.value != 0 and raw.QtyInLiters != 0:
			rate=float(raw.value)/float(raw.QtyInLiters)
		else:
			rate=0
		record=[raw.product.product,raw.name,raw.product.date,raw.product.sn,round((float(d)*float(raw.QtyInLiters)),4),round(raw.QtyInLiters,4),round(rate,4),round(raw.value,4)]

		row_num += 1
		for col_num in range(len(record)):
			ws.write(row_num, col_num, record[col_num], font_style)
	wb.save(response)
	return response

@csrf_exempt
def RawConsumptionFilter(request):
	year=request.POST['year']
	month=request.POST['month']
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	# print(days)
	consumptions=Consumption.objects.all().order_by('product')
	products=[]
	for i in consumptions:
		
		date1=datetime.strptime(i.date ,'%d/%m/%Y')
				
		d1=datetime(year,month,1)
		d2=datetime(year,month,days)
		
		if date1<d2 and date1>d1:
			raw=i.consumptionbaseoil_set.all()
			
			for j in raw:
				d=RawMaterials.objects.get(product=j.name).density
				rows=[]
				rows.append(j.product.product)
				
				rows.append(j.name)
				rows.append(j.product.date)
				rows.append(j.product.sn)
				rows.append(float(d)*(j.QtyInLiters))
				rows.append(j.QtyInLiters)
				if j.value != 0 or j.QtyInLiters != 0:
					rows.append(float(j.value)/float(j.QtyInLiters))
				else:
					rows.append(0)
				rows.append(j.value)
				
				products.append(rows)
				


				
					

				
	print(products)
	data={'products':products}	
	# print(data)
	return JsonResponse(data)

@csrf_exempt
def AdditivesConsumptionFilter(request):
	year=request.POST['year']
	month=request.POST['month']
	year=int(year)
	month=int(month)
	days=calendar.monthrange(year, month)[1]
	# print(days)
	consumptions=Consumption.objects.all().order_by('product')
	products=[]
	for i in consumptions:
		
		date1=datetime.strptime(i.date ,'%d/%m/%Y')
				
		d1=datetime(year,month,1)
		d2=datetime(year,month,days)
		
		if date1<d2 and date1>d1:
			raw=i.consumptionadditive_set.all()
			
			for j in raw:
				d=AllAdditives.objects.get(product=j.name).density
				rows=[]
				rows.append(j.product.product)
				
				rows.append(j.name)
				rows.append(j.product.date)
				rows.append(j.product.sn)
				rows.append(float(d)*(j.QtyInLiters))
				rows.append(j.QtyInLiters)
				if j.value != 0 or j.QtyInLiters != 0:
					rows.append(float(j.value)/float(j.QtyInLiters))
				else:
					rows.append(0)
				rows.append(j.value)
				
				products.append(rows)
							
	print(products)
	data={'products':products}	
	# print(data)
	return JsonResponse(data)
