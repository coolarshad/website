from django.db import models

# Create your models here.
class Packing(models.Model):
	# sn=models.IntegerField()
	sn=models.IntegerField(blank=True,null=True)
	date=models.CharField(max_length=25,null=True,blank=True)
	product=models.CharField(max_length=255)
	pereach=models.FloatField()
	category=models.CharField(max_length=255,blank=True,null=True)
	remarks=models.CharField(max_length=255,null=True,blank=True)
	approved=models.BooleanField(null=True,default=False)
	def __str__(self):
		return self.product


class Inventory(models.Model):
	sn=models.IntegerField(blank=True,null=True)
	date=models.CharField(max_length=255,blank=True,null=True)
	category=models.CharField(max_length=255,blank=True,null=True)
	product=models.CharField(max_length=255,blank=True,null=True)
	qty=models.FloatField(max_length=255,blank=True,null=True)
	unit=models.CharField(max_length=255,blank=True,null=True)
	rate=models.FloatField(blank=True,null=True)
	value=models.FloatField(blank=True,null=True)
	# dkSupply=models.CharField(max_length=255)
	# ksSupply=models.CharField(max_length=255)
	# perLiterPrice=models.FloatField()
	# valueDk=models.CharField(max_length=255)
	# valueKs=models.CharField(max_length=255)

	def __str__(self):
		return self.product

class SnInventory(models.Model):
	sn=models.IntegerField()

	def __str__(self):
		return str(self.sn)

class SnFinalProduct(models.Model):
	"""docstring for SnFinalProduct"""
	sn=models.IntegerField()
	def __str__(self):
		return str(self.sn)	

class FinalProduct(models.Model):
	"""docstring for FinalProduct"""
	# sn=models.IntegerField()
	sn=models.IntegerField(blank=True,null=True)
	date=models.CharField(max_length=25,blank=True,null=True)
	product=models.CharField(max_length=255,null=True,blank=True)
	packingsize=models.CharField(max_length=255,null=True,blank=True)
	bottlesperpack=models.FloatField(null=True,blank=True)
	litersperpack=models.FloatField(null=True,blank=True)
	totalqty=models.FloatField(null=True,blank=True)
	totalqtyunit=models.CharField(max_length=255,null=True,blank=True)
	qtyinliters=models.FloatField(null=True,blank=True)
	perlitercost=models.FloatField(null=True,blank=True)
	costpercase=models.FloatField(null=True,blank=True)
	dkcost=models.FloatField(null=True,blank=True)
	bottlepereac=models.CharField(max_length=255,null=True,blank=True)
	bottlepercase=models.FloatField(null=True,blank=True)
	bottlecapprice=models.CharField(max_length=255,null=True,blank=True)
	bottlecappercase=models.FloatField(null=True,blank=True)
	lablepereac=models.CharField(max_length=255,null=True,blank=True)
	labelpercase=models.FloatField(null=True,blank=True)
	cartons=models.CharField(max_length=255,null=True,blank=True)
	dkexprice=models.FloatField(null=True,blank=True)
	kscost=models.FloatField(null=True,blank=True)
	totalsp=models.FloatField(null=True,blank=True)
	remarks=models.CharField(max_length=255,null=True,blank=True)
	approved=models.BooleanField(null=True,default=False)
	def __str__(self):
		return self.product

class RawMaterials(models.Model):
	product=models.CharField(max_length=255)
	costPerLiter=models.FloatField()
	buyPricePmt=models.FloatField()
	addCost=models.FloatField()
	total=models.FloatField()
	mlToKl=models.FloatField()
	density=models.FloatField()
	remarks=models.CharField(max_length=255,null=True,blank=True)
	approved=models.BooleanField(null=True,default=False)
	def __str__(self):
		return self.product

class Consumption(models.Model):
	sn=models.IntegerField(blank=True,null=True)
	date=models.CharField(max_length=25,blank=True,null=True)
	product=models.CharField(max_length=255)
	grade=models.CharField(max_length=255)
	sae=models.CharField(max_length=255)
	netBlendingQty=models.FloatField()
	grossVolCrosscheck=models.FloatField()
	crosscheck=models.FloatField()
	totalvalue=models.FloatField(null=True,blank=True)
	perLiterCost=models.FloatField()
	remarks=models.CharField(max_length=255,null=True,blank=True)
	approved=models.BooleanField(null=True,default=False)
	# additives=models.ForeignKey(ConsumptionAdditive,on_delete=models.CASCADE)
	# baseoils=models.ForeignKey(ConsumptionBaseOil,on_delete=models.CASCADE)

	def __str__(self):
		return self.product



class ConsumptionAdditive(models.Model):
	product=models.ForeignKey(Consumption,on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=255)
	QtyInPercent=models.FloatField()
	QtyInLiters=models.FloatField()
	value=models.FloatField()

	def __str__(self):
		return self.name

class ConsumptionBaseOil(models.Model):
	product=models.ForeignKey(Consumption,on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=255)
	QtyInPercent=models.FloatField()
	QtyInLiters=models.FloatField()
	value=models.FloatField()

	def __str__(self):
		return self.name

class Blending(models.Model):
	# sn=models.IntegerField()
	product=models.CharField(max_length=255)
	grade=models.CharField(max_length=255)
	sae=models.CharField(max_length=255)
	percentCrosscheck=models.FloatField()
	perLiterCost=models.FloatField()
	# additives=models.ForeignKey(BlendingAdditive,on_delete=models.CASCADE)
	# baseoils=models.ForeignKey(BlendingBaseOil,on_delete=models.CASCADE)

	def __str__(self):
		return self.product

			
class BlendingBaseOil(models.Model):
	product=models.ForeignKey(Blending,on_delete=models.CASCADE)
	name=models.CharField(max_length=255)
	QtyInPercent=models.FloatField()
	QtyInLiters=models.FloatField()

	def __str__(self):
		return self.name

class BlendingAdditive(models.Model):
	product=models.ForeignKey(Blending,on_delete=models.CASCADE)
	name=models.CharField(max_length=255)
	QtyInPercent=models.FloatField()
	QtyInLiters=models.FloatField()

	def __str__(self):
		return self.name




class Additive(models.Model):
	date=models.CharField(max_length=255)
	product=models.CharField(max_length=255)
	netBlendingQtyLiter=models.FloatField()
	grossVolCrosscheck=models.FloatField()
	percentCrosscheck=models.FloatField()

	def __str__(self):
		return self.product


class AdditivesRaw(models.Model):
	additive=models.ForeignKey(Additive,on_delete=models.CASCADE, null=True)
	product=models.CharField(max_length=255)
	importRate=models.FloatField()
	addCost=models.FloatField()
	total=models.FloatField()
	mtToKl=models.FloatField()
	usage=models.FloatField()
	netCost=models.FloatField()

	def __str__(self):
		return self.product

class AdditivesPolymer(models.Model):
	additive=models.ForeignKey(Additive,on_delete=models.CASCADE, null=True)
	name=models.CharField(max_length=255)
	qtyInPercent=models.FloatField()
	qtyInLiters=models.FloatField()
	density=models.FloatField()
	qtyInKgs=models.FloatField()

	def __str__(self):
		return self.name

class AdditivesBaseOil(models.Model):
	additive=models.ForeignKey(Additive,on_delete=models.CASCADE,null=True)
	name=models.CharField(max_length=255)
	qtyInPercent=models.FloatField()
	qtyInLiters=models.FloatField()
	density=models.FloatField()
	qtyInKgs=models.FloatField()

	def __str__(self):
		return self.name


class AllAdditives(models.Model):
	# sn=models.CharField(max_length=255)
	product=models.CharField(max_length=255)
	crfPrice=models.FloatField()
	addCost=models.FloatField()
	costPriceInLiter=models.FloatField()
	density=models.FloatField()
	totalCost=models.FloatField()
	remarks=models.CharField(max_length=255)
	approved=models.BooleanField(null=True,default=False)
	def __str__(self):
		return self.product

class SnConsumptions(models.Model):
	sn=models.IntegerField()

	def __str__(self):
		return str(self.sn)

class SnPacking(models.Model):
	sn=models.IntegerField()

	def __str__(self):
		return str(self.sn)
