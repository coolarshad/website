from django.urls import path
from django.conf.urls import url
from costmanagement import views

app_name='costmanagement'

urlpatterns = [
    url(r'^raw/',views.Raw,name='raw'),
  	url(r'^additives/',views.Additives,name='additives'),
  	url(r'^additivesview/(?P<product>[a-zA-Z0-9]+)',views.AdditivesView,name='additivesview'),
  	url(r'^blending/',views.Blendings,name='blending'),
  	url(r'^consumption/',views.Consumptions,name='consumption'),
  	url(r'^consumptionview/(?P<product>[\w .{()}-]+)',views.ConsumptionView,name='consumptionview'),#(?P<product>[a-zA-Z0-9]+ (?P<product>[\w ]+)
  	url(r'^blendingview/(?P<product>[a-zA-Z0-9]+)',views.BlendingView,name='blendingview'),
  	url(r'^finalproduct/',views.FinalProducts,name='finalproduct'),
  	url(r'^inventory/',views.InventoryList,name='inventory'),
  	url(r'^packing/',views.Packings,name='packing'),
    # url(r'^finalproduct/',views.Raw,name='finalproduct'),
	url(r'^rawapprove/',views.ApproveRaw,name='raw_approve'),
	url(r'^additiveapprove/',views.ApproveAdditive,name='additive_approve'),
	url(r'^packingapprove/',views.ApprovePacking,name='approve_packing'),
	url(r'^consumptionapprove/',views.ApproveConsumption,name='approve_consumption'),
	url(r'^finalproductapprove/',views.ApproveFinalProduct,name='approve_final_product'),
   # save part---------------------------------------------------------
    url(r'^addraw/',views.SaveRaw,name='saveraw'),
    url(r'^addadditive/',views.SaveAdditives,name='saveadditive'),
    url(r'^addconsumption/',views.SaveConsumption,name='saveconsumption'),
    url(r'^addblending/',views.SaveBlending,name='saveblending'),
    url(r'^addfinalproduct/',views.SaveFinalProduct,name='savefinalproduct'),
    url(r'^addinventory/',views.SaveInventory,name='saveinventory'),
    url(r'^addpacking/',views.SavePacking,name='savepacking'),
    # edit part---------------------------------------------------------
    url(r'^editraw/',views.EditRaw,name='editraw'),
    url(r'^editpacking/',views.EditPacking,name='editpacking'),
    url(r'^editadditive/',views.EditAllAdditives,name='editAdditives'),
    url(r'^editcons/',views.EditConsumptions,name='editconsumptions'),
    url(r'^editfinalproduct/',views.EditFinalProduct,name='editfinalproduct'),
    url(r'^editinvproduction/',views.EditInvProduction,name='editInvProduction'),

    url(r'^alterpacking/',views.AlterPacking,name='alterPacking'),
    url(r'^alterraw/',views.AlterRaw,name='alterRawMaterials'),
    url(r'^alteradditives/',views.AlterAllAdditives,name='alterAdditives'),

    url(r'^delpacking/',views.DeletePacking,name='deletePacking'),
    url(r'^delraw/',views.DeleteRawMaterials,name='deleteRawMaterials'),
    url(r'^deladditive/',views.DeleteAdditives,name='deleteadditives'),
    url(r'^delblending/',views.DeleteConsumption,name='deleteconsumption'),
    url(r'^deletefinals/',views.DeleteFinal,name='deletefinal'),
    url(r'^deleteinv/',views.DeleteInventory,name='deleteInventory'),
    url(r'^getrate/',views.GetRate,name='getRate'),
    url(r'^alterinventory/',views.AlterInventory,name='alterInventory'),
    url(r'^getadditive/',views.GetAdditives,name='getAdditives'),
    url(r'^getconsumption/',views.GetConsumption,name='getConsumption'),
    url(r'^getfinal/',views.GetFinal,name='getFinal'),
    url(r'^getfinalall/',views.GetFinalAll,name='getFinalAll'),
    url(r'^getfinalproduct/',views.GetFinalProduct,name='getFinalProduct'),
    url(r'^filladditive/',views.FillAdditiveOil,name='fillAdditiveOil'),
    url(r'^exportconsump/',views.ExportConsumption,name='exportConsumption'),
    url(r'^exportraw/',views.ExportRaw,name='exportRaw'),
    url(r'^exportadditives/',views.ExportAdditives,name='exportAdditives'),
    url(r'^exportfinal/',views.ExportFinalProduct,name='exportFinalProduct'),
    url(r'^exportpacking/',views.ExportPacking,name='exportPacking'),
    url(r'^rawconsumption/',views.RawConsumption,name='rawConsumption'),
    url(r'^additiveconsumption/',views.AdditivesConsumption,name='additiveConsumption'),

    url(r'^exportrawconsumption/',views.ExportRawConsumption,name='exportrawconsumption'),
    url(r'^exportadditiveconsumption/',views.ExportAdditiveConsumption,name='exportadditiveconsumption'),
    url(r'^exportinventoryforproduction/',views.ExportInventoryForProduction,name='exportInventoryForProduction'),
    
    url(r'^rawconsumptionfilter/',views.RawConsumptionFilter,name='rawConsumptionFilter'),
    url(r'^additivesconsumptionfilter/',views.AdditivesConsumptionFilter,name='additivesConsumptionFilter'),
    url(r'^exportrawconsumptionfilter/(?P<year>\w*)/(?P<month>\w*)/',views.ExportRawConsumptionFilter,name='exportRawConsumptionFilter'),
    url(r'^exportadditivesconsumptionfilter/(?P<year>\w*)/(?P<month>\w*)/',views.ExportAdditivesConsumptionFilter,name='exportAdditivesConsumptionFilter'),
    ]
